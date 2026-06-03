# -*- coding: utf-8 -*-
"""
ABC Safari - Monkey Animator
File: ui/monkey_animator.py

TRUE frame-by-frame sprite loop engine.
Loads arrays of frames per state and cycles through them dynamically
while applying a smooth floating offset.
"""

import customtkinter as ctk
from PIL import Image
import os, math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROBO_DIR = os.path.join(BASE_DIR, "assets", "images", "animals", "robo")


class MonkeyAnimator:
    """True frame-by-frame sprite loop processing engine for CustomTkinter frames."""

    SIZE = (210, 270)

    # Each state maps to an ordered list of sprite filenames to cycle through
    _SEQUENCES = {
        "idle":     ["monkey_hello.png", "monkey_swinging.png"],
        "hello":    ["monkey_hello.png"],
        "talking":  ["monkey_hello.png", "monkey_happy.png"],
        "happy":    ["monkey_happy.png", "moneky_Walking.png"],
        "thinking": ["monkey_thinking.png"],
        "hint":     ["monkey_hint.png", "monkey_thinking.png"],
        "walking":  ["moneky_Walking.png", "monkey_hello.png"],
        "jumping":  ["monkey_Jumping.png", "monkey_happy.png"],
        "sleeping": ["monkey_sleeping_sprinte.png", "monkey_thinking.png"],
    }

    _EMOJI = {
        "idle": "🐵", "hello": "🐵", "talking": "🙊", "happy": "🎉",
        "thinking": "🤔", "hint": "👋", "walking": "🐒",
        "jumping": "🦧", "sleeping": "😴",
    }

    def __init__(self, parent, label, base_x, base_y):
        """
        parent  : CTk root (for .after())
        label   : CTkLabel to animate
        base_x  : centre x position
        base_y  : centre y position
        """
        self.parent = parent
        self.label = label
        self.base_x = base_x
        self.base_y = base_y
        self.state = "idle"
        self.frame_index = 0
        self.t = 0

        # Load arrays of frame images instead of breaking after first match
        self.sequences = {}
        for state_name, file_list in self._SEQUENCES.items():
            frames = self._load_frame_list(file_list)
            self.sequences[state_name] = frames if frames else None

        self._run_loop()

    def _load_frame_list(self, file_list):
        """Load every file in the list into memory as CTkImage frames."""
        loaded_frames = []
        for filename in file_list:
            # Try original, lowercase, and uppercase variants
            for variant in [filename, filename.lower(), filename.upper()]:
                p = os.path.join(ROBO_DIR, variant)
                if os.path.exists(p):
                    try:
                        img = Image.open(p).convert("RGBA").resize(
                            self.SIZE, Image.Resampling.LANCZOS)
                        loaded_frames.append(
                            ctk.CTkImage(light_image=img, dark_image=img,
                                         size=self.SIZE))
                        break  # found this file, move to next filename
                    except Exception:
                        pass
        return loaded_frames if loaded_frames else None

    def set_state(self, new_state):
        """Switch to a new animation state and reset the frame counter."""
        if new_state not in self._SEQUENCES:
            new_state = "idle"
        self.state = new_state
        self.frame_index = 0

    def _run_loop(self):
        """
        Swaps frames and applies a smooth vertical float effect simultaneously.
        Runs at 150ms per tick so frame changes are clearly visible.
        """
        try:
            current_frames = self.sequences.get(self.state)

            if current_frames:
                # 1. Calculate a soft vertical floating offset
                oy = int(10 * math.sin(self.t / 15))

                # 2. Cycle the active frame index naturally based on list length
                self.frame_index = (self.frame_index + 1) % len(current_frames)
                self.label.configure(image=current_frames[self.frame_index],
                                     text="")

                # 3. Position the element smoothly on the parent canvas layout
                self.label.place(x=self.base_x, y=self.base_y + oy,
                                 anchor="center")
            else:
                # Fallback emoji when no images are available
                emoji = self._EMOJI.get(self.state, "🐵")
                self.label.configure(image=None, text=emoji)
                oy = int(10 * math.sin(self.t / 15))
                self.label.place(x=self.base_x, y=self.base_y + oy,
                                 anchor="center")

            self.t += 1
            # 150ms frame rate makes sprite changes perfectly visible
            self.parent.after(150, self._run_loop)

        except Exception:
            pass  # Widget destroyed — stop silently


# ── Standalone test ────────────────────────────────────────

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.geometry("600x400")
    app.title("Monkey Animator Test")

    lbl = ctk.CTkLabel(app, text="🐵", font=ctk.CTkFont(size=100),
                       fg_color="transparent")
    lbl.place(x=300, y=200, anchor="center")

    anim = MonkeyAnimator(app, lbl, base_x=300, base_y=200)

    states = ["idle", "talking", "happy", "thinking", "hint",
              "walking", "jumping", "sleeping"]
    idx = [0]

    def cycle():
        s = states[idx[0] % len(states)]
        print(f"State → {s}")
        anim.set_state(s)
        idx[0] += 1
        app.after(2500, cycle)

    app.after(1000, cycle)
    app.mainloop()
