# -*- coding: utf-8 -*-
"""
ABC Safari - Controller Hub Core
File: main.py
"""

import customtkinter as ctk
import os, sys, threading

try: import ai_engine
except ImportError: ai_engine = None

try: import voice
except ImportError: voice = None

try: import score_tracker
except ImportError: score_tracker = None

from ui.welcome_screen import show_welcome_screen
from ui.game_screen import show_game_screen, shuffle_questions
from ui.score_screen import show_score_screen

SCREEN_W, SCREEN_H = 1280, 720

class ABCSafariApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ABC Safari")
        self.geometry(f"{SCREEN_W}x{SCREEN_H}")
        self.resizable(False, False)
        # Set window background to dark charcoal to prevent green color overlays
        self.configure(fg_color="#121212")
        
        self.player_name = "Explorer"
        self.difficulty = "Medium"
        self.score_session = 0
        self.question_track_idx = 0
        self.max_questions = 10
        
        self.launch_welcome_view()

    def launch_welcome_view(self):
        welcome_msg = voice.get_random_welcome() if voice else "Hi! Welcome to Safari Jungle Game. Nice to have you! Write your name and choose your difficulty level to start the game."
        show_welcome_screen(self, on_start=self._handle_onboarding_trigger, welcome_text=welcome_msg)
        self.update_idletasks()
        self.update()
        if voice:
            self.after(600, lambda: threading.Thread(target=lambda: voice.robo_say("welcome", custom_text=welcome_msg), daemon=True).start())

    def _handle_onboarding_trigger(self, raw_input_name, difficulty="Medium"):
        self.player_name = raw_input_name.strip() if raw_input_name.strip() else "Explorer"
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.max_questions = 5
        elif difficulty == "Hard":
            self.max_questions = 15
        else:
            self.max_questions = 10
            
        self.score_session = 0
        self.question_track_idx = 0
        
        # Shuffle the questions so that the alphabet animal order is randomized for the session!
        shuffle_questions()
        
        if ai_engine:
            ai_engine.set_child_name(self.player_name)
            ai_engine.start_session()
        if score_tracker:
            score_tracker.start_session()
            
        if voice:
            threading.Thread(target=lambda: voice.robo_say("game_start", name=self.player_name), daemon=True).start()
            
        self.launch_game_view()

    def launch_game_view(self):
        # Integrated central routing loop for Back, Next, Home, and End operations
        def handle_navigation_routing(action_type, current_score, absolute_target_index):
            print(f"[Debug] handle_navigation_routing: action={action_type}, score={current_score}, target={absolute_target_index}")
            self.score_session = current_score
            
            try:
                import pygame
                if pygame.mixer.get_init():
                    pygame.mixer.stop()
            except Exception: pass
            
            if action_type == "home":
                self.launch_welcome_view()
                return
            elif action_type == "end":
                self.launch_score_view()
                return
                
            if absolute_target_index < 0:
                absolute_target_index = 0
                
            if absolute_target_index >= self.max_questions:
                self.launch_score_view()
                return
                
            self.question_track_idx = absolute_target_index
            self.launch_game_view()

        def voice_mic_wrapper():
            if voice:
                captured = voice.listen_for_letter()

        show_game_screen(
            self, player_name=self.player_name, score=self.score_session,
            q_index=self.question_track_idx, on_answer=None,
            on_mic=voice_mic_wrapper, on_navigate=handle_navigation_routing,
            difficulty=self.difficulty
        )

    def launch_score_view(self):
        stars_calculated = 3
        weak_list = []
        if score_tracker:
            summary = score_tracker.get_session_summary()
            stars_calculated = summary.get("stars", 3)
            weak_list = summary.get("weak_letters", [])

        show_score_screen(
            self, player_name=self.player_name, score=self.score_session,
            stars=stars_calculated, weak_letters=weak_list,
            on_play_again=self._restart_session_trigger, on_quit=self.destroy
        )
        self.update_idletasks()
        self.update()
        if voice:
            self.after(500, lambda: threading.Thread(target=lambda: voice.robo_say("game_end", name=self.player_name), daemon=True).start())

    def _restart_session_trigger(self):
        # Shuffle the questions so that the new session is also randomized!
        shuffle_questions()
        if ai_engine: ai_engine.start_session()
        if score_tracker: score_tracker.start_session()
        self.score_session = 0
        self.question_track_idx = 0
        if voice:
            threading.Thread(target=lambda: voice.robo_say("welcome_back", name=self.player_name), daemon=True).start()
        self.launch_game_view()

if __name__ == "__main__":
    app = ABCSafariApp()
    app.geometry(f"{SCREEN_W}x{SCREEN_H}")
    app.mainloop()