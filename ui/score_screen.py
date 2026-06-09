# -*- coding: utf-8 -*-
"""
ABC Safari - Score Screen Hub
File: ui/score_screen.py
"""

import customtkinter as ctk
from PIL import Image, ImageTk
import os, math, random

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR    = os.path.join(BASE_DIR, "assets", "images")
ANIMAL_DIR = os.path.join(IMG_DIR, "animals")
UI_DIR     = os.path.join(ANIMAL_DIR, "ui")
FONT_DIR   = os.path.join(BASE_DIR, "assets", "fonts")

SCREEN_W, SCREEN_H = 1280, 720

def _font(size, weight="normal"):
    try:
        fname = "Nunito-Bold.ttf" if weight=="bold" else "Nunito-Regular.ttf"
        if os.path.exists(os.path.join(FONT_DIR, fname)):
            return ctk.CTkFont(family="Nunito", size=size, weight=weight)
    except Exception: pass
    return ctk.CTkFont(size=size, weight=weight)

class ScoreCanvas:
    """Instruction 9: Overhauled canvas that layers particles directly onto your custom background scene image."""
    def __init__(self, parent):
        self.parent = parent
        self.canvas = ctk.CTkCanvas(parent, bg="#0A1A10", highlightthickness=0, width=SCREEN_W, height=SCREEN_H)
        self.canvas.place(x=0, y=0)
        
        self.bg_photo = None
        p_bg = os.path.join(UI_DIR, "jungle_background.jpg")
        if os.path.exists(p_bg):
            img = Image.open(p_bg).convert("RGBA").resize((SCREEN_W, SCREEN_H), Image.LANCZOS)
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 120)) # Dark mask layer for visual structure contrast
            self.bg_photo = ImageTk.PhotoImage(Image.alpha_composite(img, overlay))
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            
        self.particles = []
        self._spawn_loop()
        self._animate()

    def _spawn_loop(self):
        colors = ["#FFD700","#FF6B9D","#4FC3F7","#A5D6A7","#E040FB"]
        for _ in range(12):
            self.particles.append({
                "x": random.randint(100, SCREEN_W-100), "y": float(SCREEN_H),
                "vy": -random.uniform(12, 19), "target_y": random.randint(60, 280),
                "color": random.choice(colors), "state": "rocket", "pts": []
            })
        self.parent.after(800, self._spawn_loop)

    def _animate(self):
        self.canvas.delete("fw")
        still_alive = []
        for p in self.particles:
            if p["state"] == "rocket":
                p["y"] += p["vy"]
                self.canvas.create_oval(p["x"]-3, p["y"]-3, p["x"]+3, p["y"]+3, fill=p["color"], outline="", tags="fw")
                if p["y"] <= p["target_y"]:
                    p["state"] = "burst"
                    for _ in range(30):
                        ang = random.uniform(0, 2*math.pi)
                        sp  = random.uniform(1.5, 6)
                        p["pts"].append({"x": p["x"], "y": p["y"], "vx": sp*math.cos(ang), "vy": sp*math.sin(ang), "life": random.randint(20, 35)})
                still_alive.append(p)
            elif p["state"] == "burst":
                active_pts = []
                for pt in p["pts"]:
                    pt["x"] += pt["vx"]; pt["y"] += pt["vy"]; pt["vy"] += 0.22; pt["life"] -= 1
                    if pt["life"] > 0:
                        self.canvas.create_oval(pt["x"]-2, pt["y"]-2, pt["x"]+2, pt["y"]+2, fill=p["color"], outline="", tags="fw")
                        active_pts.append(pt)
                p["pts"] = active_pts
                if active_pts: still_alive.append(p)
        self.particles = still_alive
        self.parent.after(30, self._animate)

def show_score_screen(root, player_name="Explorer", score=0, stars=0, weak_letters=None, on_play_again=None, on_quit=None):
    if hasattr(root, "_game_layout"):
        try: delattr(root, "_game_layout")
        except Exception: pass
    if weak_letters is None: weak_letters = []
    for w in root.winfo_children(): w.destroy()
    # Configure root background to match the dark canvas overlay exactly, eliminating green corner fringes on all widgets
    root.configure(fg_color="#0A1A10")

    engine = ScoreCanvas(root)

    # 3D Double Typography Header System (Jungle themed victory title)
    title_text = f"Safari Victory, {player_name}!"
    ctk.CTkLabel(root, text=title_text, font=_font(48, "bold"), text_color="#3E2723").place(relx=0.383, y=20, anchor="n")
    ctk.CTkLabel(root, text=title_text, font=_font(48, "bold"), text_color="#FFD600").place(relx=0.38, y=17, anchor="n")

    # Correct Answers Badge
    badge = ctk.CTkFrame(root, fg_color="#3E2723", bg_color="transparent", corner_radius=20, border_color="#FFD600", border_width=3, width=420, height=60)
    badge.place(relx=0.38, y=80, anchor="n")
    badge.pack_propagate(False)
    ctk.CTkLabel(badge, text=f"🐾  {score} Correct Answers!", font=_font(26, "bold"), text_color="#FFFFFF").place(relx=0.5, rely=0.5, anchor="center")

    # Load high-quality local trophy image
    p_trophy = os.path.join(UI_DIR, "trophy.png")
    trophy_img = None
    if os.path.exists(p_trophy):
        try:
            trophy_pil = Image.open(p_trophy).convert("RGBA")
            trophy_img = ctk.CTkImage(light_image=trophy_pil, dark_image=trophy_pil, size=(130, 130))
        except Exception: pass

    if trophy_img:
        ctk.CTkLabel(root, image=trophy_img, text="", fg_color="transparent").place(relx=0.38, y=160, anchor="n")

    # Star Rating Row (using high-quality local star images)
    p_star = os.path.join(UI_DIR, "star.png")
    star_img = None
    if os.path.exists(p_star):
        try:
            star_pil = Image.open(p_star).convert("RGBA")
            star_img = ctk.CTkImage(light_image=star_pil, dark_image=star_pil, size=(45, 45))
        except Exception: pass

    stars_frame = ctk.CTkFrame(root, fg_color="transparent", bg_color="transparent")
    stars_frame.place(relx=0.38, y=300, anchor="n")
    
    if star_img and stars > 0:
        for _ in range(stars):
            lbl = ctk.CTkLabel(stars_frame, image=star_img, text="", fg_color="transparent")
            lbl.pack(side="left", padx=4)
    else:
        # Fallback text stars
        star_str = "⭐" * stars + "☆" * (5 - stars)
        ctk.CTkLabel(stars_frame, text=star_str, font=_font(48, "bold"), text_color="#FFD700", fg_color="transparent").pack()

    # Error Feedback Cards Module
    if weak_letters:
        f_weak = ctk.CTkFrame(root, fg_color="#4A1010", bg_color="transparent", corner_radius=16, border_color="#FF6B9D", border_width=2, width=420, height=65)
        f_weak.place(relx=0.38, y=360, anchor="n")
        ctk.CTkLabel(f_weak, text=f"📝 Practice these:  " + " ".join(weak_letters), font=_font(22, "bold"), text_color="#FFCCBC").place(relx=0.5, rely=0.5, anchor="center")
    else:
        f_perf = ctk.CTkFrame(root, fg_color="#3E2723", bg_color="transparent", corner_radius=16, border_color="#A5D6A7", border_width=2, width=420, height=65)
        f_perf.place(relx=0.38, y=360, anchor="n")
        ctk.CTkLabel(f_perf, text="🌟 Perfect! No weak letters! 🌟", font=_font(20, "bold"), text_color="#A5D6A7").place(relx=0.5, rely=0.5, anchor="center")

    # Instruction 9: Target container configured for your custom dancing monkey animation media files
    media_panel = ctk.CTkFrame(root, fg_color="#27150C", bg_color="transparent", corner_radius=24, border_color="#FFD600", border_width=4, width=320, height=340)
    media_panel.place(relx=0.80, rely=0.42, anchor="center")
    media_panel.pack_propagate(False)
    
    # Static fallback representation. Replace label image attribute configuration with custom Tkinter GIF runtime engine logic if required.
    p_fallback = os.path.join(BASE_DIR, "assets/images/animals/robo/monkey_happy.png")
    if os.path.exists(p_fallback):
        img_fb = ctk.CTkImage(light_image=Image.open(p_fallback).convert("RGBA"), size=(312, 332))
        ctk.CTkLabel(media_panel, image=img_fb, text="", fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")
    else:
        ctk.CTkLabel(media_panel, text="🐵\n[Dance GIF Box]", font=_font(28, "bold"), text_color="#FFFFFF").place(relx=0.5, rely=0.5, anchor="center")

    # Primary Action Row (Celebratory buttons styling matching window colors)
    ctk.CTkButton(root, text="▶  Play Again", font=_font(28, "bold"), width=260, height=75, corner_radius=22, fg_color="#FFD600", hover_color="#FFA500", text_color="#3E2723", border_color="#3E2723", border_width=3, command=on_play_again, bg_color="transparent").place(relx=0.18, y=450, anchor="n")
    ctk.CTkButton(root, text="✕  Quit", font=_font(28, "bold"), width=200, height=75, corner_radius=22, fg_color="#8B4513", hover_color="#5C2E0B", text_color="#FFFFFF", border_color="#000000", border_width=3, command=on_quit, bg_color="transparent").place(relx=0.50, y=450, anchor="n")

    return root