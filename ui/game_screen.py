# -*- coding: utf-8 -*-
"""
ABC Safari - Game Screen Hub
File: ui/game_screen.py
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import os, math, random, threading, time
import voice

# ── Paths Configuration ──
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR    = os.path.join(BASE_DIR, "assets", "images")
ANIMAL_DIR = os.path.join(IMG_DIR, "animals")
ROBO_DIR   = os.path.join(ANIMAL_DIR, "robo")
UI_DIR     = os.path.join(ANIMAL_DIR, "ui")
SOUND_DIR  = os.path.join(BASE_DIR, "assets", "sounds")
FONT_DIR   = os.path.join(BASE_DIR, "assets", "fonts")

SCREEN_W, SCREEN_H = 1280, 720

# ── Sound Systems ──
try:
    import pygame
    pygame.mixer.init()
    _SND = True
except Exception:
    _SND = False

def play_sound(f):
    if not _SND: return
    p = os.path.join(SOUND_DIR, f)
    if os.path.exists(p):
        try: pygame.mixer.Sound(p).play()
        except Exception: pass

def play_animal_sound(animal_name, sound_path_hint):
    """Searches for sound files case-insensitively in the animal sound directory and plays it."""
    if not _SND: return
    
    # Stop any currently playing sounds first
    try: pygame.mixer.stop()
    except Exception: pass
    
    # 1. Try direct hint path
    p = os.path.join(BASE_DIR, sound_path_hint)
    if os.path.exists(p):
        try:
            pygame.mixer.Sound(p).play()
            return
        except Exception: pass
        
    # 2. Case-insensitive search on files in sound directory (supports things like cat (2).mp3 or lion (2).mp3)
    sound_dir = os.path.join(BASE_DIR, "assets", "sounds", "animals")
    if os.path.exists(sound_dir):
        stem = animal_name.lower()
        for fname in os.listdir(sound_dir):
            name, ext = os.path.splitext(fname)
            name_lower = name.lower()
            if stem == name_lower or name_lower.startswith(stem) or stem.startswith(name_lower):
                p = os.path.join(sound_dir, fname)
                try:
                    pygame.mixer.Sound(p).play()
                    return
                except Exception: pass

from data.questions import QUESTIONS
QUESTION_BANK = list(QUESTIONS)

def shuffle_questions():
    global QUESTION_BANK
    shuffled = list(QUESTIONS)
    random.shuffle(shuffled)
    QUESTION_BANK = shuffled

ANIMAL_EMOJI = {
    "A":"🐜","B":"🐻","C":"🐱","D":"🐶","E":"🐘","F":"🐸",
    "G":"🦒","H":"🦛","I":"🦎","J":"🐆","K":"🦘","L":"🦁",
    "M":"🐵","N":"🐦","O":"🦉","Q":"🐦","R":"🐰","S":"🐍",
    "T":"🐯","U":"🦄","V":"🦅","W":"🐋","Y":"🐃","Z":"🦓",
}

LETTER_COLORS = [
    {"fg":"#FFD700","hover":"#FFA500"},
    {"fg":"#FF8C00","hover":"#FF6347"},
    {"fg":"#4A90D9","hover":"#1E3A8A"},
    {"fg":"#FF6B9D","hover":"#C2185B"},
]

# ────────────────────────────────────────────────────────────
#  HELPERS
# ────────────────────────────────────────────────────────────

def load_font(size, weight="normal"):
    try:
        fname = "Nunito-Bold.ttf" if weight=="bold" else "Nunito-Regular.ttf"
        if os.path.exists(os.path.join(FONT_DIR, fname)):
            return ctk.CTkFont(family="Nunito", size=size, weight=weight)
    except Exception: pass
    return ctk.CTkFont(size=size, weight=weight)

def load_animal_image(path_str, animal_name=None, size=(260, 240)):
    if path_str:
        if hasattr(show_game_screen, "_image_cache") and path_str in show_game_screen._image_cache:
            try:
                img = show_game_screen._image_cache[path_str]
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
            except Exception: pass

        p = os.path.join(BASE_DIR, path_str)
        if os.path.exists(p):
            try:
                img = Image.open(p).convert("RGBA")
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
            except Exception: pass
            
    if animal_name:
        stem = animal_name.lower().replace(" ", "_").replace("-", "_")
        if os.path.exists(ANIMAL_DIR):
            for fname in os.listdir(ANIMAL_DIR):
                name, ext = os.path.splitext(fname)
                if name.lower() == stem or name.lower().replace(" ", "_").replace("-", "_") == stem:
                    p = os.path.join(ANIMAL_DIR, fname)
                    if os.path.exists(p) and ext.lower() in [".png", ".jpg", ".jpeg", ".webp"]:
                        try:
                            img = Image.open(p).convert("RGBA")
                            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
                        except Exception: pass
                    
    return None

def load_bg():
    for fname in ["jungle_background.jpg", "jungle_background.png", "welcome_background.jpg"]:
        p = os.path.join(UI_DIR, fname)
        if os.path.exists(p):
            try:
                img = Image.open(p).convert("RGBA")
                return img.resize((SCREEN_W, SCREEN_H), Image.LANCZOS)
            except Exception: pass
    return None

# ────────────────────────────────────────────────────────────
#  ANIMATED JUNGLE CANVAS
# ────────────────────────────────────────────────────────────

class JungleCanvas:
    def __init__(self, parent):
        self.parent = parent
        # Canvas background changed from green to dark charcoal
        self.canvas = ctk.CTkCanvas(parent, bg="#121212", highlightthickness=0, width=SCREEN_W, height=SCREEN_H)
        self.canvas.place(x=0, y=0)
        self.t = 0.0
        self._bg_pil = load_bg()
        
        # Load and draw background image EXACTLY ONCE to prevent layout blinking
        if self._bg_pil:
            self._bg_photo = ImageTk.PhotoImage(self._bg_pil)
            self.canvas.create_image(0, 0, image=self._bg_photo, anchor="nw", tags="background")
        else:
            self._bg_photo = None
            
        # Interactive Waterfall Water Movement Vectors
        self.water_streams = []
        for _ in range(45):
            self.water_streams.append({
                "x": random.uniform(550, 730),
                "y": random.uniform(220, 620),
                "speed": random.uniform(4.5, 9.5),
                "length": random.randint(12, 28)
            })
        self._animate()

    def _animate(self):
        self.t += 0.04
        # Delete only animation tags, keeping the background tag static and flicker-free
        self.canvas.delete("anim")
        W, H = SCREEN_W, SCREEN_H

        # Update and redraw waterfall particles
        for stream in self.water_streams:
            stream["y"] += stream["speed"]
            if stream["y"] > 620:
                stream["y"] = 220
                stream["x"] = random.uniform(550, 730)
            self.canvas.create_line(
                stream["x"], stream["y"], stream["x"], stream["y"] + stream["length"],
                fill="#E0F7FA", width=random.choice([2, 3, 4]), tags="anim"
            )

        # Hanging Jungle Vines
        for vx in range(80, W, 200):
            ofs = 14 * math.sin(self.t + vx / 200)
            self.canvas.create_line(
                vx+ofs, 0, vx+12+ofs, 70, vx+ofs, 140, vx+12+ofs, 210, vx+ofs, 280,
                fill="#1B5E20", width=6, smooth=True, tags="anim"
            )
            for ly in [70, 140, 210]:
                self.canvas.create_oval(vx+ofs-10, ly-7, vx+ofs+10, ly+7, fill="#2E7D32", outline="", tags="anim")

        # Swaying Ground Leaves
        for i in range(5):
            lx = (180+i*240+int(22*math.sin(self.t/2.5+i))) % W
            ly = H-80+16*math.sin(self.t/2+i*1.3)
            self.canvas.create_text(lx, ly, text="🍃", font=("Arial", 20), tags="anim")

        self.parent.after(40, self._animate)

# ────────────────────────────────────────────────────────────
#  CONFETTI BURST EFFECTS
# ────────────────────────────────────────────────────────────

class Particles:
    COLORS = ["#FFD700","#FF6B9D","#4FC3F7","#A5D6A7","#FF8F00"]

    def __init__(self, canvas):
        self.canvas = canvas
        self.pts = []

    def burst(self, cx, cy, n=55):
        for _ in range(n):
            a = random.uniform(0, 2*math.pi)
            s = random.uniform(4, 11)
            self.pts.append({
                "x":cx,"y":cy, "vx":s*math.cos(a),"vy":s*math.sin(a)-random.uniform(2,5),
                "life":random.randint(22,42), "color":random.choice(self.COLORS), "size":random.randint(5,13)
            })
        self._tick()

    def _tick(self):
        if not self.pts: return
        alive = []
        self.canvas.delete("confetti")
        for p in self.pts:
            p["x"]+=p["vx"]; p["y"]+=p["vy"]; p["vy"]+=0.38; p["life"]-=1
            if p["life"]>0:
                s=p["size"]
                self.canvas.create_oval(p["x"]-s, p["y"]-s, p["x"]+s, p["y"]+s, fill=p["color"], outline="", tags="confetti")
                alive.append(p)
        self.pts = alive
        if alive: self.canvas.after(28, self._tick)

# ────────────────────────────────────────────────────────────
#  JAIL BARS SYSTEM
# ────────────────────────────────────────────────────────────

class JailBars:
    def __init__(self, canvas):
        self.canvas = canvas

    def show(self, cx, cy, w=380, h=360):
        self._cx, self._cy, self._w, self._h = cx, cy, w, h
        self._drop = 0
        self._fall()

    def _fall(self):
        self._drop = min(self._drop+16, self._h)
        self.canvas.delete("jail")
        x0, y0 = self._cx - self._w//2, self._cy - self._h//2
        self.canvas.create_rectangle(x0, y0, x0+self._w, y0+14, fill="#424242", outline="#212121", width=2, tags="jail")
        for bx in range(x0+18, x0+self._w, 36):
            self.canvas.create_rectangle(bx, y0, bx+10, y0+self._drop, fill="#616161", outline="#212121", width=1, tags="jail")
        if self._drop < self._h: self.canvas.after(20, self._fall)
        else: self.canvas.after(1400, lambda: self.canvas.delete("jail"))

# ────────────────────────────────────────────────────────────
#  PROGRESS SCORE BAR (Refactored using transparent CTkProgressBar)
# ────────────────────────────────────────────────────────────

class ScoreBar:
    MAX = 10
    def __init__(self, parent, x, y, w=300, h=24):
        self.parent = parent
        self.w = w
        self.h = h
        self.pbar = ctk.CTkProgressBar(parent, width=w, height=h, fg_color="#0C240E", progress_color="#FFD600", corner_radius=6, border_width=0)
        self.pbar.place(x=x, y=y, anchor="nw")
        self.pbar.set(0.0)

    def update(self, s):
        val = min(s, self.MAX) / self.MAX
        self.pbar.set(val)

# ────────────────────────────────────────────────────────────
#  MAIN INTERFACE GENERATION MODULE
# ────────────────────────────────────────────────────────────

def show_game_screen(parent, player_name="Explorer", score=0, q_index=0, on_answer=None, on_mic=None, on_navigate=None, difficulty="Medium"):
    root = parent
    # Configure root with a dark charcoal background
    root.configure(fg_color="#121212")

    # Filter QUESTION_BANK by difficulty parameter
    filtered_bank = [q for q in QUESTION_BANK if q.get("difficulty") == difficulty]
    if not filtered_bank:
        filtered_bank = list(QUESTION_BANK)

    COL1_X, COL1_W, COL3_X, CARD_Y, CARD_H, BTN_W, BTN_H = 45, 330, 980, 120, 380, 125, 110
    QUESTION_PROMPTS = [
        "What letter does\n{animal} start with?",
        "Which letter makes the\nfirst sound of {animal}?",
        "Can you find the\nstarting letter for {animal}?",
        "What letter does the\n{animal} begin with?",
        "Help me find the\nfirst letter of {animal}!",
        "Look at the {animal}!\nWhat is its starting letter?",
        "Which letter is for the\n{animal}?",
        "Choose the correct\nstarting letter for {animal}!"
    ]

    # ────────────────────────────────────────────────────────────
    #  CASE 1: Flicker-Free Update (Layout Cache already exists)
    # ────────────────────────────────────────────────────────────
    if hasattr(parent, "_game_layout"):
        layout = parent._game_layout
        
        # Stop any active sounds immediately before updating the view
        if _SND:
            try: pygame.mixer.stop()
            except Exception: pass

        # Clean up any leftover canvas jail overlay or cry text to prevent them bleeding into the next question
        layout["canvas"].delete("jail")
        layout["canvas"].delete("cry")

        # Update internal state
        layout["state"]["score"] = score
        layout["state"]["wrong"] = 0
        layout["state"]["answered"] = False

        # Update question details
        q = filtered_bank[q_index % len(filtered_bank)]
        cor = q["letter"]

        # Choices selection
        all_l = list(set([x["letter"] for x in filtered_bank]))
        if cor not in all_l: all_l.append(cor)
        other_letters = [l for l in all_l if l != cor]
        if len(other_letters) < 3:
            other_letters = [l for l in [chr(i) for i in range(65, 91)] if l != cor]
        choices = random.sample(other_letters, 3) + [cor]
        random.shuffle(choices)

        # Pre-loading next question's animal image
        next_index = (q_index + 1) % len(filtered_bank)
        next_q = filtered_bank[next_index]
        if not hasattr(show_game_screen, "_image_cache"):
            show_game_screen._image_cache = {}

        def preload_next_image():
            try:
                nxt_img_path = next_q["image"]
                p = os.path.join(BASE_DIR, nxt_img_path)
                if os.path.exists(p):
                    img = Image.open(p).convert("RGBA").resize((260, 240), Image.Resampling.LANCZOS)
                    show_game_screen._image_cache[nxt_img_path] = img
            except Exception: pass

        threading.Thread(target=preload_next_image, daemon=True).start()

        # Update animal card image & fallback
        animal_img = load_animal_image(q["image"], animal_name=q["animal"], size=(260, 240))
        fallback_char = q.get("emoji", ANIMAL_EMOJI.get(cor, "🐾"))

        layout["animal_lbl"].configure(
            image=animal_img or None,
            text=fallback_char if not animal_img else "",
            font=ctk.CTkFont(size=130 if not animal_img else 50)
        )
        layout["banner_lbl"].configure(text=q["animal"])

        # Update score indicators
        layout["score_var"].set(f"Score: {score} ⭐")
        layout["sb"].update(score)

        # Update bubble prompt question
        template = QUESTION_PROMPTS[q_index % len(QUESTION_PROMPTS)]
        bubble_question = template.replace("{animal}", q['animal'])
        layout["robo_text"].set(bubble_question)

        # Define click actions for options
        def navigate_and_stop(action_type, target_idx):
            print(f"[Debug] navigate_and_stop in Case 1 called: action={action_type}, target={target_idx}")
            if _SND:
                try: pygame.mixer.stop()
                except Exception: pass
            if on_navigate:
                score_to_pass = 0 if action_type == "home" else layout["state"]["score"]
                on_navigate(action_type, score_to_pass, target_idx)

        def on_click(letter, btn, cidx, skip_voice=False):
            if layout["state"]["answered"]: return

            for b in layout["btns"]:
                try: b.configure(state="disabled")
                except Exception: pass

            if letter == cor:
                layout["state"]["answered"] = True
                layout["state"]["score"] += 1
                layout["score_var"].set(f"Score: {layout['state']['score']} ⭐")
                layout["sb"].update(layout["state"]["score"])

                if btn:
                    if btn.cget("image"):
                        btn.configure(image=None)
                    btn.configure(fg_color="#4CAF50", border_color="#FFFFFF", border_width=4)
                    layout["parts"].burst(btn.winfo_x() + BTN_W//2, btn.winfo_y() + BTN_H//2, 60)

                # Play animal sound immediately (non-blocking)
                play_animal_sound(q["animal"], q["sound"])

                if not skip_voice:
                    def _voice_c():
                        try: voice.robo_say_correct(name=player_name, count=layout["state"]["score"])
                        except Exception: pass
                    root.after(400, lambda: threading.Thread(target=_voice_c, daemon=True).start())

                # Autonavigate instantly (100ms delay)
                root.after(100, lambda: navigate_and_stop("next", q_index + 1))
            else:
                layout["state"]["wrong"] += 1
                if btn:
                    if btn.cget("image"):
                        btn.configure(image=None)
                    btn.configure(fg_color="#FF6B35")

                    def restore_btn():
                        try:
                            c = LETTER_COLORS[cidx]
                            p_img = os.path.join(BASE_DIR, "assets", "images", "ui", f"btn_jungle_{cidx+1}.png")
                            if not os.path.exists(p_img):
                                p_img = os.path.join(UI_DIR, f"btn_jungle_{cidx+1}.png")
                            if os.path.exists(p_img):
                                pil_img = Image.open(p_img).convert("RGBA").resize((BTN_W, BTN_H), Image.Resampling.LANCZOS)
                                btn_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(BTN_W, BTN_H))
                                btn.configure(image=btn_img, fg_color="transparent", state="normal")
                            else:
                                btn.configure(fg_color=c["fg"], state="normal")
                        except Exception: pass
                        re_enable_buttons(-1)

                    root.after(900, restore_btn)
                    play_sound("wrong.wav")

                    if not skip_voice:
                        def _voice_w():
                            try: voice.robo_say("wrong_random", name=player_name)
                            except Exception: pass
                        root.after(400, lambda: threading.Thread(target=_voice_w, daemon=True).start())
                else:
                    layout["state"]["answered"] = True
                    play_sound("wrong.wav")
                    root.after(100, lambda: navigate_and_stop("next", q_index + 1))

                layout["jail"].show(COL1_X + COL1_W//2, CARD_Y + CARD_H//2, COL1_W-20, CARD_H-20)
                layout["canvas"].create_text(COL1_X + COL1_W//2, CARD_Y + CARD_H//2 - 20, text="😭", font=("Arial", 80), tags="cry")
                layout["canvas"].after(1500, lambda: layout["canvas"].delete("cry"))

        def re_enable_buttons(wrong_btn_idx):
            for i, b in enumerate(layout["btns"]):
                if i != wrong_btn_idx:
                    try: b.configure(state="normal")
                    except Exception: pass

        def trigger_hint():
            if layout["state"]["answered"]: return
            threading.Thread(target=lambda: voice.robo_say("hint", letter=cor, animal=q["animal"]), daemon=True).start()

            correct_btn = None
            for idx, b in enumerate(layout["btns"]):
                if b.cget("text") == cor:
                    correct_btn = b
                    break
            if correct_btn:
                original_border_width = correct_btn.cget("border_width")
                original_border_color = correct_btn.cget("border_color")
                original_image = correct_btn.cget("image")
                pulse_colors = ["#FFD700", "#FFC107", "#FFB300", "#FFA000"]
                pulse_state = [0]
                def pulse():
                    if pulse_state[0] < 10 and not layout["state"]["answered"]:
                        color = pulse_colors[pulse_state[0] % len(pulse_colors)]
                        correct_btn.configure(border_width=6, border_color=color)
                        pulse_state[0] += 1
                        root.after(300, pulse)
                    else:
                        try: correct_btn.configure(border_width=original_border_width, border_color=original_border_color, image=original_image)
                        except Exception: pass
                pulse()

        root.bind("<h>", lambda e: trigger_hint())
        root.bind("<H>", lambda e: trigger_hint())

        layout["hint_btn"].configure(command=trigger_hint)

        # Update options buttons
        for i, b in enumerate(layout["btns"]):
            c = LETTER_COLORS[i]
            b.configure(text=choices[i], state="normal")

            p_img = os.path.join(BASE_DIR, "assets", "images", "ui", f"btn_jungle_{i+1}.png")
            if not os.path.exists(p_img):
                p_img = os.path.join(UI_DIR, f"btn_jungle_{i+1}.png")

            if os.path.exists(p_img):
                try:
                    pil_img = Image.open(p_img).convert("RGBA").resize((BTN_W, BTN_H), Image.Resampling.LANCZOS)
                    btn_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(BTN_W, BTN_H))
                    b.configure(image=btn_img, fg_color="transparent", border_width=0)
                except Exception:
                    b.configure(image=None, fg_color=c["fg"], border_color="#000000", border_width=3)
            else:
                b.configure(image=None, fg_color=c["fg"], border_color="#000000", border_width=3)

            b.configure(command=lambda l=choices[i], btn=b, ci=i: on_click(l, btn, ci))

        # Reconfigure nav bar commands with default parameter bindings to fix late-binding bugs
        layout["back_btn"].configure(command=lambda target=q_index: navigate_and_stop("back", target - 1))
        layout["next_btn"].configure(command=lambda target=q_index: navigate_and_stop("next", target + 1))
        layout["home_btn"].configure(command=lambda: navigate_and_stop("home", 0))
        layout["end_btn"].configure(command=lambda target=q_index: navigate_and_stop("end", target))

        # Update speech recognition handler variables
        def handle_spoken_letter(letter):
            if layout["state"]["answered"]: return
            letter = letter.upper()
            try:
                if pygame.mixer.get_init():
                    pygame.mixer.stop()
            except Exception: pass
            is_correct = (letter == cor)
            def SpeakFeedback():
                try:
                    time.sleep(0.4)
                    if is_correct:
                        voice.robo_say("mic_correct")
                    else:
                        feedback = f"You said {letter}. That is not correct! Try another option!"
                        voice.robo_say(None, custom_text=feedback)
                except Exception: pass
            threading.Thread(SpeakFeedback, daemon=True).start()

            found_btn = None
            found_idx = -1
            for idx, choice in enumerate(choices):
                if choice == letter:
                    found_btn = layout["btns"][idx]
                    found_idx = idx
                    break
            if found_btn:
                on_click(letter, found_btn, found_idx, skip_voice=True)
            else:
                if letter == cor:
                    for idx, choice in enumerate(choices):
                        if choice == cor:
                            on_click(cor, layout["btns"][idx], idx, skip_voice=True)
                            break
                else:
                    on_click(letter, None, -1, skip_voice=True)

        def run_mic_backend():
            try:
                captured = voice.listen_for_letter()
                print(f"[Debug] run_mic_backend captured in Case 1: {captured}")
                if captured:
                    root.after(0, lambda: handle_spoken_letter(captured))
                    root.after(0, lambda: layout["mic_lbl"].configure(text=f"Heard: {captured}!"))
                    root.after(2200, reset_mic_ui)
                else:
                    root.after(0, lambda: layout["mic_lbl"].configure(text="No sound detected"))
                    root.after(0, reset_mic_ui) # Reset layout immediately on failure
                    threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
            except OSError as e:
                print(f"Mic device error: {e}")
                root.after(0, lambda: layout["mic_lbl"].configure(text="Error: No mic found!"))
                root.after(0, reset_mic_ui)
                threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
            except ValueError as e:
                print(f"Mic value error: {e}")
                root.after(0, lambda: layout["mic_lbl"].configure(text=str(e)))
                root.after(0, reset_mic_ui)
                threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
            except ConnectionError as e:
                print(f"Mic connection error: {e}")
                root.after(0, lambda: layout["mic_lbl"].configure(text="Error: No Internet!"))
                root.after(0, reset_mic_ui)
                threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
            except Exception as e:
                print(f"Mic error: {e}")
                root.after(0, lambda: layout["mic_lbl"].configure(text=f"Error: {str(e)}"))
                root.after(0, reset_mic_ui)
                threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()

        def reset_mic_ui():
            layout["mic_state"]["on"] = False
            layout["mic_btn"].configure(fg_color="#FFF9C4", text_color="#E65100", text="🎤")
            layout["mic_lbl"].configure(text="Say the letter!")

        def toggle_mic():
            if not layout["mic_state"]["on"]:
                layout["mic_state"]["on"] = True
                # Active recording button turns Red instead of Green to remove green colors
                layout["mic_btn"].configure(fg_color="#FF5252", text_color="#FFFFFF", text="🛑")
                layout["mic_lbl"].configure(text="Listening...")
                threading.Thread(target=run_mic_backend, daemon=True).start()
            else:
                reset_mic_ui()

        layout["mic_btn"].configure(command=toggle_mic)

        return parent

    # ────────────────────────────────────────────────────────────
    #  CASE 2: First Load (Construct Widgets from scratch)
    # ────────────────────────────────────────────────────────────
    for w in parent.winfo_children():
        w.destroy()

    # Base Canvas and Background Overlays
    jungle = JungleCanvas(root)
    
    # Force instant render to prevent white flashes
    root.update_idletasks()
    
    parts  = Particles(jungle.canvas)
    jail   = JailBars(jungle.canvas)

    q = filtered_bank[q_index % len(filtered_bank)]
    cor = q["letter"]

    state = {
        "score":    score,
        "wrong":    0,
        "answered": False,
    }

    all_l = list(set([x["letter"] for x in filtered_bank]))
    if cor not in all_l: all_l.append(cor)
    other_letters = [l for l in all_l if l != cor]
    if len(other_letters) < 3:
        other_letters = [l for l in [chr(i) for i in range(65, 91)] if l != cor]
    choices = random.sample(other_letters, 3) + [cor]
    random.shuffle(choices)

    # ── Header HUD Configuration (Background changed to transparent to remove solid colors) ──
    hdr = ctk.CTkFrame(root, fg_color="transparent", bg_color="transparent", border_color="#FFD600", border_width=3, corner_radius=16, width=SCREEN_W-80, height=80)
    hdr.place(x=40, y=15)
    hdr.pack_propagate(False)
    
    # Scale Up brand logo asset to prominent 150x80 size
    logo_path = os.path.join(UI_DIR, "logo_main.png")
    if os.path.exists(logo_path):
        logo_pil = Image.open(logo_path).resize((150, 80), Image.Resampling.LANCZOS)
        logo_mini = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(150, 80))
        logo_icon = ctk.CTkLabel(hdr, image=logo_mini, text="", fg_color="transparent")
        logo_icon.place(x=15, y=0)
        
        name_lbl = ctk.CTkLabel(hdr, text=f"Explorer: {player_name}", font=load_font(24, "bold"), text_color="#FFFFFF", fg_color="transparent")
        name_lbl.place(x=185, y=25)
    else:
        ctk.CTkLabel(hdr, text=f"🐾 Explorer: {player_name}", font=load_font(24,"bold"), text_color="#FFFFFF", fg_color="transparent").place(x=18, y=25)
        
    sb = ScoreBar(hdr, x=SCREEN_W//2-170, y=28, w=260, h=24)
    sb.update(score)
    
    score_var = ctk.StringVar(value=f"Score: {score} ⭐")
    ctk.CTkLabel(hdr, textvariable=score_var, font=load_font(24, "bold"), text_color="#FFD600", fg_color="transparent").place(x=SCREEN_W-260, y=22)

    # ── Column 1: Animal Card Hub ──
    # Shadow frame color changed from dark green to dark charcoal shadow
    ctk.CTkFrame(root, fg_color="#090909", bg_color="transparent", corner_radius=26, width=COL1_W, height=CARD_H).place(x=COL1_X+6, y=CARD_Y+6)
    card = ctk.CTkFrame(root, fg_color="#FFFFFF", bg_color="transparent", corner_radius=24, border_color="#FFD600", border_width=5, width=COL1_W, height=CARD_H)
    card.place(x=COL1_X, y=CARD_Y)

    # Search for image using path from question data
    animal_img = load_animal_image(q["image"], animal_name=q["animal"], size=(260, 240))
    fallback_char = q.get("emoji", ANIMAL_EMOJI.get(cor, "🐾"))
    
    animal_lbl = ctk.CTkLabel(
        card,
        image=animal_img or None,
        text=fallback_char if not animal_img else "",
        font=ctk.CTkFont(size=130 if not animal_img else 50),
        fg_color="transparent"
    )
    animal_lbl.place(relx=0.5, y=15, anchor="n")

    # Card banner uses dark brown outline but no bright green backgrounds
    banner = ctk.CTkFrame(card, fg_color="#8B4513", bg_color="transparent", corner_radius=14, border_color="#FFD600", border_width=2, width=270, height=50)
    banner.place(relx=0.5, y=295, anchor="n")
    banner_lbl = ctk.CTkLabel(banner, text=q['animal'], font=load_font(24,"bold"), text_color="#FFFFFF", fg_color="transparent")
    banner_lbl.place(relx=0.5, rely=0.5, anchor="center")

    # Prompt Speech Bubble Frame
    template = QUESTION_PROMPTS[q_index % len(QUESTION_PROMPTS)]
    bubble_question = template.replace("{animal}", q['animal'])

    bubble = ctk.CTkFrame(root, fg_color="#FFFDE7", bg_color="transparent", corner_radius=18, border_color="#FFD54F", border_width=3, width=340, height=80)
    bubble.place(relx=0.5, y=100, anchor="n")
    robo_text = ctk.StringVar(value=bubble_question)
    # Changed text color from green to dark charcoal
    ctk.CTkLabel(bubble, textvariable=robo_text, font=load_font(18, "bold"), text_color="#333333", wraplength=320, justify="center").place(relx=0.5, rely=0.5, anchor="center")

    # Re-instantiate static Monkey Label holding transparent robo.png (centered in grid to avoid overlap)
    monkey_lbl = ctk.CTkLabel(root, text="", fg_color="transparent")
    monkey_x, monkey_y = 830, 350
    
    p_robo = os.path.join(ROBO_DIR, "robo.png")
    if os.path.exists(p_robo):
        try:
            pil_robo = Image.open(p_robo).convert("RGBA").resize((210, 270), Image.Resampling.LANCZOS)
            robo_ctk_img = ctk.CTkImage(light_image=pil_robo, dark_image=pil_robo, size=(210, 270))
            monkey_lbl.configure(image=robo_ctk_img)
        except Exception as ex:
            print(f"Error loading robo.png: {ex}")
            monkey_lbl.configure(text="🐵", font=ctk.CTkFont(size=100))
    else:
        monkey_lbl.configure(text="🐵", font=ctk.CTkFont(size=100))
        
    monkey_lbl.place(x=monkey_x, y=monkey_y, anchor="center")

    # ── Column 3: Matrix Choice Letter Buttons ──
    btn_positions = [
        (COL3_X,     140), (COL3_X+140, 140),
        (COL3_X,     275), (COL3_X+140, 275),
    ]
    btns = []

    def re_enable_buttons(wrong_btn_idx):
        for i, b in enumerate(btns):
            if i != wrong_btn_idx:
                try: b.configure(state="normal")
                except Exception: pass

    def navigate_and_stop(action_type, target_idx):
        print(f"[Debug] navigate_and_stop in Case 2 called: action={action_type}, target={target_idx}")
        if _SND:
            try: pygame.mixer.stop()
            except Exception: pass
        if on_navigate:
            score_to_pass = 0 if action_type == "home" else state["score"]
            on_navigate(action_type, score_to_pass, target_idx)

    def on_click(letter, btn, cidx, skip_voice=False):
        if state["answered"]: return

        for b in btns:
            try: b.configure(state="disabled")
            except Exception: pass

        if letter == cor:
            state["answered"] = True
            state["score"] += 1
            score_var.set(f"Score: {state['score']} ⭐")
            sb.update(state["score"])

            if btn:
                if btn.cget("image"):
                    btn.configure(image=None)
                btn.configure(fg_color="#4CAF50", border_color="#FFFFFF", border_width=4)
                parts.burst(btn.winfo_x() + BTN_W//2, btn.winfo_y() + BTN_H//2, 60)
            
            # Play animal sound immediately (non-blocking)
            play_animal_sound(q["animal"], q["sound"])

            if not skip_voice:
                def _voice_c():
                    try: voice.robo_say_correct(name=player_name, count=state["score"])
                    except Exception: pass
                root.after(400, lambda: threading.Thread(target=_voice_c, daemon=True).start())
            
            # Autonavigate instantly (100ms)
            root.after(100, lambda: navigate_and_stop("next", q_index + 1))
        else:
            state["wrong"] += 1

            if btn:
                if btn.cget("image"):
                    btn.configure(image=None)
                btn.configure(fg_color="#FF6B35")

                def restore_btn():
                    try:
                        c = LETTER_COLORS[cidx]
                        p_img = os.path.join(BASE_DIR, "assets", "images", "ui", f"btn_jungle_{cidx+1}.png")
                        if not os.path.exists(p_img):
                            p_img = os.path.join(UI_DIR, f"btn_jungle_{cidx+1}.png")
                            
                        if os.path.exists(p_img):
                            pil_img = Image.open(p_img).convert("RGBA").resize((BTN_W, BTN_H), Image.Resampling.LANCZOS)
                            btn_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(BTN_W, BTN_H))
                            btn.configure(image=btn_img, fg_color="transparent", state="normal")
                        else:
                            btn.configure(fg_color=c["fg"], state="normal")
                    except Exception: pass
                    re_enable_buttons(-1)

                root.after(900, restore_btn)
                play_sound("wrong.wav")
                
                if not skip_voice:
                    def _voice_w():
                        try: voice.robo_say("wrong_random", name=player_name)
                        except Exception: pass
                    root.after(400, lambda: threading.Thread(target=_voice_w, daemon=True).start())
            else:
                state["answered"] = True
                play_sound("wrong.wav")
                root.after(100, lambda: navigate_and_stop("next", q_index + 1))

            jail.show(COL1_X + COL1_W//2, CARD_Y + CARD_H//2, COL1_W-20, CARD_H-20)
            jungle.canvas.create_text(COL1_X + COL1_W//2, CARD_Y + CARD_H//2 - 20, text="😭", font=("Arial", 80), tags="cry")
            jungle.canvas.after(1500, lambda: jungle.canvas.delete("cry"))

    # Helper to add floating effect on hover
    def make_btn_float(btn, orig_x, orig_y):
        def on_enter(event):
            if btn.cget("state") == "normal":
                btn.place(x=orig_x, y=orig_y - 8)
        def on_leave(event):
            btn.place(x=orig_x, y=orig_y)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # Load button background images
    for i, (x, y) in enumerate(btn_positions):
        c = LETTER_COLORS[i]
        
        btn_img = None
        p_img = os.path.join(BASE_DIR, "assets", "images", "ui", f"btn_jungle_{i+1}.png")
        if not os.path.exists(p_img):
            p_img = os.path.join(UI_DIR, f"btn_jungle_{i+1}.png")
            
        if os.path.exists(p_img):
            try:
                pil_img = Image.open(p_img).convert("RGBA").resize((BTN_W, BTN_H), Image.Resampling.LANCZOS)
                btn_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(BTN_W, BTN_H))
            except Exception as ex:
                print(f"Error loading jungle button background: {ex}")

        # Hover color changed from green to dark slate
        if btn_img:
            b = ctk.CTkButton(root, text=choices[i], image=btn_img, font=load_font(52, "bold"), width=BTN_W, height=BTN_H,
                corner_radius=22, fg_color="transparent", hover_color="#263238", text_color="#FFFFFF", border_width=0,
                bg_color="transparent")
        else:
            b = ctk.CTkButton(root, text=choices[i], font=load_font(52, "bold"), width=BTN_W, height=BTN_H,
                corner_radius=22, fg_color=c["fg"], hover_color=c["hover"], text_color="#FFFFFF", border_color="#000000", border_width=3,
                bg_color="transparent")

        b.place(x=x, y=y, anchor="nw")
        b.configure(command=lambda l=choices[i], btn=b, ci=i: on_click(l, btn, ci))
        make_btn_float(b, x, y)
        btns.append(b)

    # Hint Button trigger logic
    def trigger_hint():
        if state["answered"]: return
        threading.Thread(target=lambda: voice.robo_say("hint", letter=cor, animal=q["animal"]), daemon=True).start()
        
        # Find correct button
        correct_btn = None
        for idx, b in enumerate(btns):
            if b.cget("text") == cor:
                correct_btn = b
                break
                
        if correct_btn:
            original_border_width = correct_btn.cget("border_width")
            original_border_color = correct_btn.cget("border_color")
            original_image = correct_btn.cget("image")
            pulse_colors = ["#FFD700", "#FFC107", "#FFB300", "#FFA000"]
            pulse_state = [0]
            
            def pulse():
                if pulse_state[0] < 10 and not state["answered"]:
                    color = pulse_colors[pulse_state[0] % len(pulse_colors)]
                    correct_btn.configure(border_width=6, border_color=color)
                    pulse_state[0] += 1
                    root.after(300, pulse)
                else:
                    try: correct_btn.configure(border_width=original_border_width, border_color=original_border_color, image=original_image)
                    except Exception: pass
            pulse()

    # Bind 'h' / 'H' keys for hint trigger
    root.bind("<h>", lambda e: trigger_hint())
    root.bind("<H>", lambda e: trigger_hint())

    # ── Speech Recognition Handler ──
    def handle_spoken_letter(letter):
        if state["answered"]: return
        letter = letter.upper()
        
        try:
            if pygame.mixer.get_init():
                pygame.mixer.stop()
        except Exception: pass

        is_correct = (letter == cor)
        
        def SpeakFeedback():
            try:
                time.sleep(0.4)
                if is_correct:
                    voice.robo_say("mic_correct")
                else:
                    feedback = f"You said {letter}. That is not correct! Try another option!"
                    voice.robo_say(None, custom_text=feedback)
            except Exception: pass

        threading.Thread(SpeakFeedback, daemon=True).start()

        found_btn = None
        found_idx = -1
        for idx, choice in enumerate(choices):
            if choice == letter:
                found_btn = btns[idx]
                found_idx = idx
                break
        
        if found_btn:
            on_click(letter, found_btn, found_idx, skip_voice=True)
        else:
            if letter == cor:
                for idx, choice in enumerate(choices):
                    if choice == cor:
                        on_click(cor, btns[idx], idx, skip_voice=True)
                        break
            else:
                on_click(letter, None, -1, skip_voice=True)

    # ── Concurrency-Isolated Microphone Input Module ──
    mic_state = {"on": False}
    mic_btn = ctk.CTkButton(root, text="🎤", width=65, height=65, corner_radius=32,
        font=load_font(24,"bold"), fg_color="#FFF9C4", hover_color="#FFF176", text_color="#E65100", border_color="#FFD54F", border_width=3,
        bg_color="transparent")
    mic_btn.place(x=40, y=SCREEN_H-30, anchor="sw")

    mic_lbl = ctk.CTkLabel(root, text="Say the letter!", font=load_font(14,"bold"), text_color="#FFFDE7", fg_color="transparent", bg_color="transparent")
    mic_lbl.place(x=120, y=SCREEN_H-50, anchor="sw")

    def run_mic_backend():
        try:
            captured = voice.listen_for_letter()
            print(f"[Debug] run_mic_backend captured in Case 2: {captured}")
            if captured:
                root.after(0, lambda: handle_spoken_letter(captured))
                root.after(0, lambda: mic_lbl.configure(text=f"Heard: {captured}!"))
                root.after(2200, reset_mic_ui)
            else:
                root.after(0, lambda: mic_lbl.configure(text="No sound detected"))
                root.after(0, reset_mic_ui) # Reset layout immediately on failure
                threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
        except OSError as e:
            print(f"Mic device error: {e}")
            root.after(0, lambda: mic_lbl.configure(text="Error: No mic found!"))
            root.after(0, reset_mic_ui)
            threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
        except ValueError as e:
            print(f"Mic value error: {e}")
            root.after(0, lambda: mic_lbl.configure(text=str(e)))
            root.after(0, reset_mic_ui)
            threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
        except ConnectionError as e:
            print(f"Mic connection error: {e}")
            root.after(0, lambda: mic_lbl.configure(text="Error: No Internet!"))
            root.after(0, reset_mic_ui)
            threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()
        except Exception as e:
            print(f"Mic error: {e}")
            root.after(0, lambda: mic_lbl.configure(text=f"Error: {str(e)}"))
            root.after(0, reset_mic_ui)
            threading.Thread(target=lambda: voice.robo_say("mic_fail"), daemon=True).start()

    def reset_mic_ui():
        mic_state["on"] = False
        mic_btn.configure(fg_color="#FFF9C4", text_color="#E65100", text="🎤")
        mic_lbl.configure(text="Say the letter!")

    def toggle_mic():
        if not mic_state["on"]:
            mic_state["on"] = True
            # Active recording turns Red instead of Green to remove green background colors
            mic_btn.configure(fg_color="#FF5252", text_color="#FFFFFF", text="🛑")
            mic_lbl.configure(text="Listening...")
            threading.Thread(target=run_mic_backend, daemon=True).start()
        else:
            reset_mic_ui()
            
    mic_btn.configure(command=toggle_mic)

    # ── Global Navigation Control Bar System (Background changed to transparent to remove solid colors) ──
    nav_bar = ctk.CTkFrame(root, fg_color="transparent", bg_color="transparent", border_color="#FFD600", border_width=2, corner_radius=14, height=65, width=640)
    nav_bar.place(relx=0.5, y=SCREEN_H-30, anchor="s")
    nav_bar.pack_propagate(False)

    # Buttons color changed from green to gold/orange to match theme and fit beautifully
    back_btn = ctk.CTkButton(nav_bar, text="◀ BACK", font=load_font(16, "bold"), fg_color="#FFB300", hover_color="#FFA000", text_color="#000000", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda target=q_index: navigate_and_stop("back", target - 1))
    back_btn.place(x=15, y=12)
    
    next_btn = ctk.CTkButton(nav_bar, text="NEXT ▶", font=load_font(16, "bold"), fg_color="#FFB300", hover_color="#FFA000", text_color="#000000", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda target=q_index: navigate_and_stop("next", target + 1))
    next_btn.place(x=140, y=12)

    # HINT button placed directly inside the main navigation card between NEXT and HOME (eliminating overlap)
    hint_btn = ctk.CTkButton(nav_bar, text="💡 HINT", font=load_font(16, "bold"), fg_color="#FF9800", hover_color="#E65100", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=trigger_hint)
    hint_btn.place(x=265, y=12)

    home_btn = ctk.CTkButton(nav_bar, text="🏠 HOME", font=load_font(16, "bold"), fg_color="#FFB300", hover_color="#FFA000", text_color="#000000", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda: navigate_and_stop("home", 0))
    home_btn.place(x=390, y=12)

    end_btn = ctk.CTkButton(nav_bar, text="🛑 END", font=load_font(16, "bold"), fg_color="#FFB300", hover_color="#FFA000", text_color="#000000", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda target=q_index: navigate_and_stop("end", target))
    end_btn.place(x=515, y=12)

    # Countdown timer completely removed as requested

    # Save references to widgets for subsequent updates
    parent._game_layout = {
        "state": state,
        "canvas": jungle.canvas,
        "parts": parts,
        "jail": jail,
        "sb": sb,
        "score_var": score_var,
        "robo_text": robo_text,
        "animal_lbl": animal_lbl,
        "banner_lbl": banner_lbl,
        "btns": btns,
        "hint_btn": hint_btn,
        "back_btn": back_btn,
        "next_btn": next_btn,
        "home_btn": home_btn,
        "end_btn": end_btn,
        "mic_btn": mic_btn,
        "mic_lbl": mic_lbl,
        "mic_state": mic_state
    }

    return root

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = ctk.CTk()
    app.title("ABC Safari - Game Screen")
    app.geometry(f"{SCREEN_W}x{SCREEN_H}")
    app.resizable(False, False)

    def _ans(correct, new_score, next_index):
        pass
    def _nav(action, score, idx):
        print(f"Nav action: {action} target idx: {idx}")

    show_game_screen(app, "Sajjad", 0, 0, _ans, on_navigate=_nav)
    app.mainloop()