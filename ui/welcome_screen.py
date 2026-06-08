# -*- coding: utf-8 -*-
"""
ABC Safari - Welcome Screen
File: ui/welcome_screen.py

UPDATED: Integrated a live, multi-asset realistic butterfly flight engine
with automatic error handling fallbacks.
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import os, math, random

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR    = os.path.join(BASE_DIR, "assets", "images")
ANIMAL_DIR = os.path.join(IMG_DIR, "animals")
ROBO_DIR   = os.path.join(ANIMAL_DIR, "robo")
UI_DIR     = os.path.join(ANIMAL_DIR, "ui")
FONT_DIR   = os.path.join(BASE_DIR, "assets", "fonts")

SCREEN_W, SCREEN_H = 1280, 720


def _font(size, weight="normal"):
    try:
        fname = "Nunito-Bold.ttf" if weight == "bold" else "Nunito-Regular.ttf"
        if os.path.exists(os.path.join(FONT_DIR, fname)):
            return ctk.CTkFont(family="Nunito", size=size, weight=weight)
    except Exception:
        pass
    return ctk.CTkFont(size=size, weight=weight)


def _load_pil(filename, dirs):
    for d in dirs:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            try:
                return Image.open(p).convert("RGBA")
            except Exception:
                pass
    return None


# ── Overlay canvas for animated elements (vines, sun, butterflies, etc.) ──
class JungleOverlay:
    """Draws animated overlays on a tkinter Canvas placed above the bg label."""

    def __init__(self, parent):
        self.parent = parent
        self.canvas = ctk.CTkCanvas(parent, highlightthickness=0,
                                    width=SCREEN_W, height=SCREEN_H)
        self.canvas.place(x=0, y=0)
        self.t = 0.0
        
        # Load background image
        self.bg_photo = None
        bg_path = os.path.join(UI_DIR, "welcome_background.jpg")
        if not os.path.exists(bg_path):
            bg_path = os.path.join(UI_DIR, "welcome_background.png")
        if os.path.exists(bg_path):
            try:
                bg_pil = Image.open(bg_path).resize((SCREEN_W, SCREEN_H), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_pil)
            except Exception: pass

        # Load logo image to draw directly on canvas (prevents green borders)
        self.logo_photo = None
        logo_path = os.path.join(UI_DIR, "logo_main.png")
        if os.path.exists(logo_path):
            try:
                logo_pil = Image.open(logo_path).resize((220, 120), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_pil)
            except Exception: pass

        # 🦋 REAL BUTTERFLY ANIMATION SYSTEM INITIALIZATION 🦋
        self.bf_photos = []  # Holds hard references to protect from garbage collection
        self._load_butterfly_assets()
        
        # Generate a flock of 5 distinct butterflies with random starting positions and flight speeds
        self.flock = []
        for _ in range(5):
            self.flock.append({
                "x": random.uniform(100, SCREEN_W - 100),
                "y": random.uniform(100, SCREEN_H - 100),
                "vx": random.uniform(-2.0, 2.0),
                "vy": random.uniform(-1.5, 1.5),
                "frame": random.randint(0, 1)
            })
            
        self._animate()

    def _load_butterfly_assets(self):
        """Pre-loads wings-up and wings-down frames into standard Tkinter PhotoImages."""
        for fname in ["butterfly_1.png", "butterfly_2.png"]:
            pil_img = _load_pil(fname, [UI_DIR])
            if pil_img:
                resized = pil_img.resize((45, 45), Image.Resampling.LANCZOS)
                self.bf_photos.append(ImageTk.PhotoImage(resized))

    def _animate(self):
        self.t += 0.04
        self.canvas.delete("a")
        W, H = SCREEN_W, SCREEN_H

        # Draw Background
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="a")

        # Draw Logo directly on Canvas (completely transparent background, no green borders)
        if self.logo_photo:
            self.canvas.create_image(140, 75, image=self.logo_photo, anchor="center", tags="a")
        else:
            self.canvas.create_text(140, 75, text="🌿  ABC Safari  🌿", font=_font(32, "bold"), fill="#3E2723", tags="a")

        # 1. Vines Animation
        for vx in range(80, W, 200):
            ofs = 16 * math.sin(self.t + vx / 200)
            self.canvas.create_line(
                vx + ofs, 0, vx + 13 + ofs, 75, vx + ofs, 150,
                vx + 13 + ofs, 225, vx + ofs, 300,
                fill="#1B5E20", width=7, smooth=True, tags="a")
            for ly in [75, 150, 225]:
                self.canvas.create_oval(
                    vx + ofs - 13, ly - 8, vx + ofs + 13, ly + 8,
                    fill="#388E3C", outline="", tags="a")

        # 2. Sun Animation (moved to the right side of the screen)
        sun_x = W - 160
        sy = 55 + 5 * math.sin(self.t * 0.6)
        self.canvas.create_oval(sun_x - 28, sy - 28, sun_x + 28, sy + 28,
                                fill="#FFD54F", outline="#FFC107", width=3, tags="a")
        for ang in range(0, 360, 45):
            r = math.radians(ang)
            self.canvas.create_line(
                sun_x + 34 * math.cos(r), sy + 34 * math.sin(r),
                sun_x + 48 * math.cos(r), sy + 48 * math.sin(r),
                fill="#FFC107", width=3, tags="a")

        # 3. Swinging monkey emoji decoration (DELETED)

        # 4. 🦋 REAL BUTTERFLY FLIGHT ENGINE (Flies around from here to there!) 🦋
        for b in self.flock:
            # Apply a random, jittery force to mimic real, organic insect motion
            b["vx"] += random.uniform(-0.3, 0.3)
            b["vy"] += random.uniform(-0.3, 0.3)
            
            # Speed control clamping
            b["vx"] = max(-3.5, min(3.5, b["vx"]))
            b["vy"] = max(-2.5, min(2.5, b["vy"]))
            
            # Apply physics updates
            b["x"] += b["vx"]
            b["y"] += b["vy"]
            
            # Screen boundary wrap-around safety
            if b["x"] < -60: b["x"] = W + 60
            if b["x"] > W + 60: b["x"] = -60
            if b["y"] < -60: b["y"] = H + 60
            if b["y"] > H + 60: b["y"] = -60
            
            # Alternate flapping frame rate steps
            if int(self.t * 10) % 3 == 0:
                b["frame"] = (b["frame"] + 1) % 2

            # Render image if assets are present, otherwise execute safe beautiful emoji fallback
            if len(self.bf_photos) >= 2:
                self.canvas.create_image(b["x"], b["y"], image=self.bf_photos[b["frame"]], tags="a")
            else:
                self.canvas.create_text(b["x"], b["y"], text="🦋", font=("Arial", 32), tags="a")

        # 5. Parrot Animation
        px = 55 + 7 * math.sin(self.t * 0.5)
        py = 290 + 9 * math.cos(self.t * 0.8)
        self.canvas.create_text(px, py, text="\U0001F99C",
                                font=("Arial", 42), tags="a")

        # 6. Waterfall Animation (DELETED from welcome screen)

        # 7. Falling Leaves Animation
        for i in range(5):
            lx = (190 + i * 220 + int(28 * math.sin(self.t / 3 + i))) % W
            ly = H - 88 + 22 * math.sin(self.t / 2 + i * 1.3)
            self.canvas.create_text(lx, ly, text="\U0001F343",
                                    font=("Arial", 24), tags="a")

        self.parent.after(42, self._animate)


class FloatRobo:
    def __init__(self, parent, lbl):
        self.parent = parent
        self.lbl = lbl
        self.s = 0
        self._go()

    def _go(self):
        try:
            oy = int(16 * math.sin(self.s / 52))
            self.lbl.place(relx=0.73,
                           rely=0.53 + oy / SCREEN_H, anchor="center")
            self.s += 1
            self.parent.after(35, self._go)
        except Exception:
            pass


class BubblePulse:
    COLS = ["#FFD54F", "#FF8F00", "#FFD54F", "#81C784"]

    def __init__(self, parent, frm):
        self.parent = parent
        self.frm = frm
        self.i = 0
        self._go()

    def _go(self):
        try:
            self.frm.configure(border_color=self.COLS[self.i % len(self.COLS)])
            self.i += 1
            self.parent.after(600, self._go)
        except Exception:
            pass


class StarBurst:
    def __init__(self, canvas):
        self.canvas = canvas
        self.pts = []
        self.running = False

    def burst(self, cx, cy, n=18):
        self.pts = []
        for _ in range(n):
            a = random.uniform(0, 2 * math.pi)
            sp = random.uniform(3, 8)
            self.pts.append({
                "x": cx, "y": cy,
                "vx": sp * math.cos(a), "vy": sp * math.sin(a),
                "life": random.randint(18, 30),
                "color": random.choice(["#FFD700", "#FF6B9D", "#4FC3F7",
                                        "#A5D6A7", "#FF8F00"]),
                "size": random.randint(5, 12)})
        self.running = True
        self._tick()

    def _tick(self):
        if not self.running:
            return
        alive = []
        for p in self.pts:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.25
            p["life"] -= 1
            if p["life"] > 0:
                s = p["size"]
                self.canvas.create_oval(
                    p["x"] - s, p["y"] - s, p["x"] + s, p["y"] + s,
                    fill=p["color"], outline="", tags="burst")
                alive.append(p)
        self.pts = alive
        if alive:
            self.canvas.after(30, lambda: (
                self.canvas.delete("burst"), self._tick()))
        else:
            self.running = False


# ────────────────────────────────────────────────────────────
#  MAIN FUNCTION
# ────────────────────────────────────────────────────────────

def show_welcome_screen(root, on_start=None):
    for w in root.winfo_children():
        w.destroy()
    root.configure(fg_color="#1E4620")

    # ── Animated overlay (places canvas, draws background and logo directly on canvas) ──
    overlay = JungleOverlay(root)

    # ── Whiteboard Name Card Area (Solid white background with brown/gold border and rounded transparent corners) ──
    card_frame = ctk.CTkFrame(
        root, fg_color="#FFFFFF", bg_color="transparent", corner_radius=24,
        border_color="#8B4513", border_width=4, width=420, height=220
    )
    card_frame.place(relx=0.50, rely=0.52, anchor="center")
    card_frame.pack_propagate(False)
    
    ctk.CTkLabel(
        card_frame, text="👋  Welcome, Explorer!",
        font=_font(26, "bold"), text_color="#3E2723"
    ).pack(pady=(15, 5))

    ctk.CTkLabel(
        card_frame, text="What is your name?",
        font=_font(20), text_color="#5D4037"
    ).pack(pady=(0, 6))

    name_var = ctk.StringVar()
    entry = ctk.CTkEntry(
        card_frame, textvariable=name_var,
        placeholder_text="Type your name here...",
        font=_font(20, "bold"), width=380, height=52,
        corner_radius=14, fg_color="#FFFFFF",
        border_color="#8B4513", border_width=3,
        text_color="#3E2723"
    )
    entry.pack(padx=24, pady=6)
    entry.focus()

    def start():
        n = name_var.get().strip() or "Explorer"
        if on_start:
            on_start(n)

    btn = ctk.CTkButton(
        card_frame, text="▶  START ADVENTURE",
        font=_font(22, "bold"), width=260, height=44,
        corner_radius=20, fg_color="#FF9800",
        hover_color="#E65100", text_color="#FFFFFF",
        border_color="#FFD54F", border_width=3,
        command=start, bg_color="transparent"
    )
    btn.pack(pady=10)
    entry.bind("<Return>", lambda e: start())

    # ── Speech Bubble Placement ──
    bubble = ctk.CTkFrame(root, fg_color="#FFFDE7", bg_color="transparent", corner_radius=18,
                          border_color="#FFD54F", border_width=3,
                          width=460, height=65)
    bubble.place(relx=0.5, y=640, anchor="n")
    
    ctk.CTkLabel(bubble,
                 text="Hi! 🌴  I'm Robo! Let's learn the alphabet!\nType your name and press START!",
                 font=_font(15, "bold"), text_color="#4E342E",
                 wraplength=430).place(relx=0.5, rely=0.5, anchor="center")
    BubblePulse(root, bubble)

    # ── Star burst ──
    sb = StarBurst(overlay.canvas)
    btn.bind("<Enter>", lambda e: sb.burst(
        int(root.winfo_width() * 0.42), 430))

    return root


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = ctk.CTk()
    app.title("ABC Safari - Welcome")
    app.geometry(f"{SCREEN_W}x{SCREEN_H}")
    app.resizable(False, False)
    show_welcome_screen(app, on_start=lambda n: print(f"Start: {n}"))
    app.mainloop()