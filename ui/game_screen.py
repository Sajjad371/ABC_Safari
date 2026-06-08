# -*- coding: utf-8 -*-
"""
ABC Safari - Game Screen Hub
File: ui/game_screen.py

Features:
- Removed old-fashioned black HUD bar for an organic green layout frame
- Scaled up the header logo image asset to match the text profile
- Removed the static monkey frame container to reveal the background scenery
- Added thread-safe microphone listening logic to prevent application freezing
- Integrated live canvas line particle arrays for an animated waterfall flow effect
- Mounted BACK, NEXT, HOME, and END controls onto a unified navigation bar
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import os, math, random, threading

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

from data.questions import QUESTIONS
QUESTION_BANK = QUESTIONS

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


def load_animal_image(path_str, size=(290, 290)):
    if not path_str: return None
    p = os.path.join(BASE_DIR, path_str)
    if os.path.exists(p):
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
        self.canvas = ctk.CTkCanvas(parent, bg="#2E7D32", highlightthickness=0, width=SCREEN_W, height=SCREEN_H)
        self.canvas.place(x=0, y=0)
        self.t = 0.0
        self._bg_pil   = load_bg()
        self._bg_photo = None
        
        # Interactive Waterfall Water Movement Vectors Array (Instruction 7)
        # Positioned to align with the background image's center waterfall (x: 550 to 730, y: 220 to 620)
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
        self.canvas.delete("anim")
        W, H = SCREEN_W, SCREEN_H

        if self._bg_pil:
            photo = ImageTk.PhotoImage(self._bg_pil)
            self._bg_photo = photo
            self.canvas.create_image(0, 0, image=photo, anchor="nw")

        # Render and update moving animated water flow stream particles over the graphics
        for stream in self.water_streams:
            stream["y"] += stream["speed"]
            if stream["y"] > 620:
                stream["y"] = 220
                stream["x"] = random.uniform(550, 730)
            self.canvas.create_line(
                stream["x"], stream["y"], stream["x"], stream["y"] + stream["length"],
                fill="#E0F7FA", width=random.choice([2, 3, 4]), tags="anim"
            )

        # Hanging Jungle Vines Path Loops
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
            self.canvas.create_text(lx, ly, text="\U0001F343", font=("Arial", 20), tags="anim")

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
#  PROGRESS SCORE BAR
# ────────────────────────────────────────────────────────────

class ScoreBar:
    MAX = 10
    def __init__(self, parent, x, y, w=300, h=24):
        self.parent=parent; self.w=w; self.h=h; self._score=0; self._disp=0.0
        self.cv = ctk.CTkCanvas(parent, width=w, height=h, bg="#3E2723", highlightthickness=0)
        self.cv.place(x=x, y=y, anchor="nw")
        self._draw()

    def update(self, s):
        self._score = min(s, self.MAX)
        self._fill()

    def _fill(self):
        tgt = self._score / self.MAX
        cur = self._disp / self.w
        if cur < tgt:
            self._disp = min(self._disp + self.w/28, tgt*self.w)
            self._draw()
            self.parent.after(20, self._fill)
        else: self._draw()

    def _draw(self):
        self.cv.delete("all")
        self.cv.create_rectangle(0, 0, self.w, self.h, fill="#27150C", outline="")
        fw = int(self._disp)
        if fw > 0:
            self.cv.create_rectangle(0, 0, fw, self.h, fill="#FFD600", outline="")

# ────────────────────────────────────────────────────────────
#  MAIN INTERFACE GENERATION MODULE
# ────────────────────────────────────────────────────────────

def show_game_screen(parent, player_name="Explorer", score=0, q_index=0, on_answer=None, on_mic=None, on_navigate=None):
    for w in parent.winfo_children():
        w.destroy()

    root = parent
    root.configure(fg_color="#3E2723")

    state = {
        "score":    score,
        "wrong":    0,
        "answered": False,
    }

    q   = QUESTION_BANK[q_index % len(QUESTION_BANK)]
    cor = q["letter"]

    all_l   = [x["letter"] for x in QUESTION_BANK]
    choices = random.sample([l for l in all_l if l != cor], 3) + [cor]
    random.shuffle(choices)

    # COL1_W reduced to 330, CARD_H reduced to 380, COL3_X moved to 980 to reveal background characters
    COL1_X, COL1_W, COL3_X, CARD_Y, CARD_H, BTN_W, BTN_H = 45, 330, 980, 120, 380, 125, 110

    # Base Canvas and Overlays
    jungle = JungleCanvas(root)
    parts  = Particles(jungle.canvas)
    jail   = JailBars(jungle.canvas)

    # ── Header HUD Configuration (with bg_color="transparent") ──
    hdr = ctk.CTkFrame(root, fg_color="#3E2723", bg_color="transparent", border_color="#FFD600", border_width=3, corner_radius=16, width=SCREEN_W-80, height=80)
    hdr.place(x=40, y=15)
    hdr.pack_propagate(False)
    
    # Instruction 5: Scaled Up Large Game Logo Brand Asset
    logo_path = os.path.join(UI_DIR, "logo_main.png")
    if os.path.exists(logo_path):
        logo_pil = Image.open(logo_path).resize((110, 60), Image.Resampling.LANCZOS)
        logo_mini = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(110, 60))
        logo_icon = ctk.CTkLabel(hdr, image=logo_mini, text="", fg_color="transparent")
        logo_icon.place(x=15, y=8)
        
        name_lbl = ctk.CTkLabel(hdr, text=f"Explorer: {player_name}", font=load_font(24, "bold"), text_color="#FFFFFF", fg_color="transparent")
        name_lbl.place(x=140, y=22)
    else:
        ctk.CTkLabel(hdr, text=f"🐾 Explorer: {player_name}", font=load_font(24,"bold"), text_color="#FFFFFF", fg_color="transparent").place(x=18, y=22)
        
    sb = ScoreBar(hdr, x=SCREEN_W//2-170, y=28, w=260, h=24)
    sb.update(score)
    
    score_var = ctk.StringVar(value=f"Score: {score} ⭐")
    ctk.CTkLabel(hdr, textvariable=score_var, font=load_font(24, "bold"), text_color="#FFD600", fg_color="transparent").place(x=SCREEN_W-260, y=22)

    # ── Column 1: Animal Card Hub (with bg_color="transparent" to remove white corners) ──
    ctk.CTkFrame(root, fg_color="#27150C", bg_color="transparent", corner_radius=26, width=COL1_W, height=CARD_H).place(x=COL1_X+6, y=CARD_Y+6)
    card = ctk.CTkFrame(root, fg_color="#FFFFFF", bg_color="transparent", corner_radius=24, border_color="#FFD600", border_width=5, width=COL1_W, height=CARD_H)
    card.place(x=COL1_X, y=CARD_Y)

    animal_img = load_animal_image(q["image"], size=(260, 240))
    animal_lbl = ctk.CTkLabel(card, image=animal_img or None, text=ANIMAL_EMOJI.get(cor,"🐾") if not animal_img else "", font=ctk.CTkFont(size=110), fg_color="transparent")
    animal_lbl.place(relx=0.5, y=15, anchor="n")

    # Banner resized to fit inside the narrower card
    banner = ctk.CTkFrame(card, fg_color="#1B5E20", bg_color="transparent", corner_radius=14, border_color="#FFD600", border_width=2, width=270, height=50)
    banner.place(relx=0.5, y=295, anchor="n")
    ctk.CTkLabel(banner, text=q['animal'], font=load_font(24,"bold"), text_color="#FFFFFF", fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    # Prompt Speech Bubble Frame placed centered in the sky above the waterfall
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
    template = QUESTION_PROMPTS[q_index % len(QUESTION_PROMPTS)]
    bubble_question = template.replace("{animal}", q['animal'])
    spoken_question = bubble_question.replace("\n", " ")

    bubble = ctk.CTkFrame(root, fg_color="#FFFDE7", bg_color="transparent", corner_radius=18, border_color="#FFD54F", border_width=3, width=340, height=80)
    bubble.place(relx=0.5, y=100, anchor="n")
    robo_text = ctk.StringVar(value=bubble_question)
    ctk.CTkLabel(bubble, textvariable=robo_text, font=load_font(18, "bold"), text_color="#4E342E", wraplength=320, justify="center").place(relx=0.5, rely=0.5, anchor="center")

    # ── Column 3: Matrix Choice Letter Buttons (Positioned to reveal characters on right cliff) ──
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

    # Wrapper for handling transitions and stopping sounds
    def navigate_and_stop(action_type, target_idx):
        if _SND:
            try: pygame.mixer.stop()
            except Exception: pass
        if on_navigate:
            score_to_pass = 0 if action_type == "home" else state["score"]
            on_navigate(action_type, score_to_pass, target_idx)

    def on_click(letter, btn, cidx):
        if state["answered"]: return

        for b in btns:
            try: b.configure(state="disabled")
            except Exception: pass

        if letter == cor:
            state["answered"] = True
            state["score"] += 1
            score_var.set(f"Score: {state['score']} ⭐")
            sb.update(state["score"])
            btn.configure(fg_color="#4CAF50", border_color="#FFFFFF", border_width=4)
            play_sound("correct.wav")
            parts.burst(btn.winfo_x() + BTN_W//2, btn.winfo_y() + BTN_H//2, 60)
            robo_text.set(f"AMAZING! {cor} is for {q['animal']}! 🌟")

            # Play the animal sound ONLY when correct answer is clicked
            if _SND:
                p_sound = os.path.join(BASE_DIR, q["sound"])
                if os.path.exists(p_sound):
                    try: pygame.mixer.Sound(p_sound).play()
                    except Exception: pass

            # Instruction 1: Thread-safe voice invocation prevents premature audio cuts
            def _voice_c():
                try:
                    import voice
                    voice.robo_say_correct(name=player_name, count=state["score"])
                except Exception: pass
            root.after(400, lambda: threading.Thread(target=_voice_c, daemon=True).start())
            
            # Autonavigate triggers after complete phrase voice playback buffer clears (increased to 3000ms)
            root.after(3000, lambda: navigate_and_stop("next", q_index + 1))
        else:
            state["wrong"] += 1
            btn.configure(fg_color="#FF6B35")

            def restore_btn():
                try: btn.configure(fg_color=LETTER_COLORS[cidx]["fg"], state="normal")
                except Exception: pass
                re_enable_buttons(-1)

            root.after(900, restore_btn)
            play_sound("wrong.wav")

            jail.show(COL1_X + COL1_W//2, CARD_Y + CARD_H//2, COL1_W-20, CARD_H-20)
            jungle.canvas.create_text(COL1_X + COL1_W//2, CARD_Y + CARD_H//2 - 20, text="😭", font=("Arial", 80), tags="cry")
            jungle.canvas.after(1500, lambda: jungle.canvas.delete("cry"))

            # Instruction 4: Uses dynamic random expressions via "wrong_random" key
            def _voice_w():
                try:
                    import voice
                    voice.robo_say("wrong_random", name=player_name)
                except Exception: pass
            root.after(400, lambda: threading.Thread(target=_voice_w, daemon=True).start())

    for i, (x, y) in enumerate(btn_positions):
        c = LETTER_COLORS[i]
        b = ctk.CTkButton(root, text=choices[i], font=load_font(52, "bold"), width=BTN_W, height=BTN_H,
            corner_radius=22, fg_color=c["fg"], hover_color=c["hover"], text_color="#FFFFFF", border_color="#000000", border_width=3,
            bg_color="transparent")
        b.place(x=x, y=y, anchor="nw")
        b.configure(command=lambda l=choices[i], btn=b, ci=i: on_click(l, btn, ci))
        btns.append(b)

    # ── Speech Recognition Handler ──
    def handle_spoken_letter(letter):
        if state["answered"]: return
        letter = letter.upper()
        found_btn = None
        found_idx = -1
        for idx, choice in enumerate(choices):
            if choice == letter:
                found_btn = btns[idx]
                found_idx = idx
                break
        
        if found_btn:
            on_click(letter, found_btn, found_idx)
        else:
            if letter == cor:
                for idx, choice in enumerate(choices):
                    if choice == cor:
                        on_click(cor, btns[idx], idx)
                        break

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
            import voice
            if voice:
                captured = voice.listen_for_letter()
                if captured:
                    root.after(0, lambda: handle_spoken_letter(captured))
                    root.after(0, lambda: mic_lbl.configure(text=f"Heard: {captured}!"))
                else:
                    root.after(0, lambda: mic_lbl.configure(text="No sound detected"))
        except OSError as e:
            print(f"Mic device error: {e}")
            root.after(0, lambda: mic_lbl.configure(text="Error: No mic found!"))
        except ValueError as e:
            print(f"Mic value error: {e}")
            root.after(0, lambda: mic_lbl.configure(text=str(e)))
        except ConnectionError as e:
            print(f"Mic connection error: {e}")
            root.after(0, lambda: mic_lbl.configure(text="Error: No Internet!"))
        except Exception as e:
            print(f"Mic error: {e}")
            root.after(0, lambda: mic_lbl.configure(text=f"Error: {str(e)}"))
        root.after(2200, reset_mic_ui)

    def reset_mic_ui():
        mic_state["on"] = False
        mic_btn.configure(fg_color="#FFF9C4", text="🎤")
        mic_lbl.configure(text="Say the letter!")

    def toggle_mic():
        if not mic_state["on"]:
            mic_state["on"] = True
            mic_btn.configure(fg_color="#4CAF50", text="🛑")
            mic_lbl.configure(text="Listening...")
            threading.Thread(target=run_mic_backend, daemon=True).start()
        else:
            reset_mic_ui()
            
    mic_btn.configure(command=toggle_mic)

    # ── Global Navigation Control Bar System (matching BACK/NEXT colors) ──
    nav_bar = ctk.CTkFrame(root, fg_color="#3E2723", bg_color="transparent", border_color="#FFD600", border_width=2, corner_radius=14, height=65, width=640)
    nav_bar.place(relx=0.5, y=SCREEN_H-30, anchor="s")
    nav_bar.pack_propagate(False)

    ctk.CTkButton(nav_bar, text="◀ BACK", font=load_font(16, "bold"), fg_color="#8B4513", hover_color="#5C2E0B", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda: navigate_and_stop("back", q_index - 1)).place(x=15, y=12)
    
    ctk.CTkButton(nav_bar, text="NEXT ▶", font=load_font(16, "bold"), fg_color="#8B4513", hover_color="#5C2E0B", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda: navigate_and_stop("next", q_index + 1)).place(x=140, y=12)

    ctk.CTkButton(nav_bar, text="🏠 HOME", font=load_font(16, "bold"), fg_color="#8B4513", hover_color="#5C2E0B", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda: navigate_and_stop("home", 0)).place(x=390, y=12)

    ctk.CTkButton(nav_bar, text="🛑 END", font=load_font(16, "bold"), fg_color="#8B4513", hover_color="#5C2E0B", width=110, height=40, corner_radius=10, bg_color="transparent",
                  command=lambda: navigate_and_stop("end", q_index)).place(x=515, y=12)

    def _trig():
        try:
            import voice
            threading.Thread(target=voice.robo_say, kwargs={"line_key": "question", "custom_text": spoken_question}, daemon=True).start()
        except Exception: pass
    root.after(400, _trig)

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
        print(f"Nav action triggered: {action} target idx: {idx}")

    show_game_screen(app, "Sajjad", 0, 0, _ans, on_navigate=_nav)
    app.mainloop()