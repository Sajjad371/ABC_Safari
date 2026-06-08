"""
============================================================
  Robo's Jungle ABC — Voice Engine (Member 5 Contribution)
  CCC1243 Artificial Intelligence | Group Project
  Albukhary International University
============================================================

  WHAT THIS FILE DOES
  -------------------
  This module handles ALL voice features for Robo's Jungle ABC:

    1. VOICE INPUT  — SpeechRecognition
       Listens to the child's voice via microphone for 3 seconds.
       Sends audio to Google Web Speech API.
       Returns a clean lowercase string (e.g. "l" or "lion").
       Passes that string to the game logic — same as a button press.

    2. VOICE OUTPUT — pyttsx3 (offline) with gTTS (online upgrade)
       Makes Robo speak: questions, praise, hints, child's name.
       Always runs in a separate background thread so the UI NEVER freezes.

    3. FALLBACK SAFETY
       If mic fails → game still works via click buttons (always shown).
       If gTTS is unavailable (no internet) → pyttsx3 takes over silently.
       If pyttsx3 also fails → game continues without speech.

  HOW OTHER MEMBERS CONNECT TO THIS FILE
  ---------------------------------------
    from voice_engine import VoiceEngine
    robo_voice = VoiceEngine(child_name="Amir")

    # Member 5 calls (from mic button press):
    spoken = robo_voice.listen()          # returns "l" or None

    # Member 1 calls (AI logic triggers hints):
    robo_voice.speak_hint("L", "Lion")

    # Member 2 calls (UI triggers praise/question):
    robo_voice.speak_praise("L")
    robo_voice.speak_question("Lion")

    # Member 3 calls (game logic triggers wrong feedback):
    robo_voice.speak_wrong("L")

  INSTALL COMMANDS (run once before first use)
  --------------------------------------------
    pip install SpeechRecognition
    pip install pyaudio
    pip install pyttsx3
    pip install gTTS
    pip install playsound==1.2.2   (needed by gTTS player)

  NOTE: pyaudio can be tricky on Windows. If it fails, use:
    pip install pipwin
    pipwin install pyaudio

============================================================
"""

import speech_recognition as sr
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except Exception:
    pyttsx3 = None
    PYTTSX3_AVAILABLE = False

import threading
import time
import os
import tempfile
from typing import Optional

# ── Optional gTTS import (graceful fallback if not installed) ──
try:
    from gtts import gTTS
    import playsound
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════
#   VOICE ENGINE CLASS
# ═══════════════════════════════════════════════════════════════

class VoiceEngine:
    """
    Central voice controller for Robo's Jungle ABC.

    Create ONE instance when the game starts and reuse it throughout.
    All speech runs in background threads — the UI is never blocked.

    Parameters
    ----------
    child_name : str
        The child's name entered on the welcome screen.
        Robo uses this in praise phrases ("Great job, Amir!").
    use_gtts : bool
        True  → try gTTS first (warmer, more natural voice, needs internet).
        False → use pyttsx3 only (always offline).
        Default is True — falls back to pyttsx3 if internet is missing.
    listen_seconds : int
        How long Robo listens after the mic button is pressed.
        Default 3 seconds is enough for a single letter or short word.
    """

    def __init__(self, child_name: str = "Friend", use_gtts: bool = True,
                 listen_seconds: int = 3):

        self.child_name    = child_name.strip().capitalize()
        self.use_gtts      = use_gtts and GTTS_AVAILABLE
        self.listen_seconds = listen_seconds

        # ── SpeechRecognition setup ────────────────────────────
        self.recognizer = sr.Recognizer()

        # Adjust for ambient noise automatically before each listen
        self.recognizer.dynamic_energy_threshold = True
        # Lower pause threshold = faster response after child stops speaking
        self.recognizer.pause_threshold = 0.6

        # ── pyttsx3 setup ──────────────────────────────────────
        # This is built once and reused — creating a new engine each
        # time causes a memory leak, especially on long game sessions.
        if PYTTSX3_AVAILABLE:
            try:
                self._pyttsx3_engine = pyttsx3.init()
                self._configure_pyttsx3()
                self._pyttsx3_ok = True
            except Exception:
                self._pyttsx3_engine = None
                self._pyttsx3_ok = False
        else:
            self._pyttsx3_engine = None
            self._pyttsx3_ok = False  # game still works without TTS

        # ── Thread lock ───────────────────────────────────────
        # Prevents two speech calls from overlapping (e.g. fast tapping)
        self._speech_lock = threading.Lock()

        # ── Mic availability flag ─────────────────────────────
        self.mic_available = self._check_microphone()

    # ───────────────────────────────────────────────────────────
    #   INTERNAL SETUP HELPERS
    # ───────────────────────────────────────────────────────────

    def _configure_pyttsx3(self):
        """Set Robo's voice to a clear, slightly slower speed for children."""
        engine = self._pyttsx3_engine

        # Speed: default is ~200. Slower = easier for young children to follow.
        engine.setProperty("rate", 150)

        # Volume: maximum clarity
        engine.setProperty("volume", 1.0)

        # Voice: prefer a female voice if available — tends to sound friendlier
        voices = engine.getProperty("voices")
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.id.lower():
                engine.setProperty("voice", voice.id)
                break  # stop after finding the first female voice

    def _check_microphone(self) -> bool:
        """
        Quietly test whether a microphone is accessible.
        Returns True if a mic is found, False otherwise.
        Called once during __init__ — result stored in self.mic_available.
        """
        try:
            with sr.Microphone() as _:
                return True
        except (OSError, AttributeError):
            return False

    # ───────────────────────────────────────────────────────────
    #   PUBLIC METHOD 1 — VOICE INPUT (SpeechRecognition)
    # ───────────────────────────────────────────────────────────

    def listen(self, prompt_ui_callback=None) -> Optional[str]:
        """
        Listen to the child's spoken answer via microphone.

        Called by Member 2's UI when the microphone button is pressed.

        Parameters
        ----------
        prompt_ui_callback : callable, optional
            A function from Member 2's UI code that updates a label like
            "Robo is listening... 🎤". Called immediately before listening
            starts so the child gets visual feedback right away.

        Returns
        -------
        str or None
            Recognised word/letter as a lowercase stripped string.
            e.g. "l", "lion", "a", "apple"
            Returns None if:
              - No microphone is connected
              - Child said nothing / too quiet
              - Google could not understand the audio
              - No internet connection (Google API requires internet)

        How the return value is used
        ----------------------------
            spoken = robo_voice.listen()
            if spoken is not None:
                game_logic.check_answer(spoken)   # same path as button click
            # If None → game simply waits; child can use click buttons instead
        """
        if not self.mic_available:
            print("[VoiceEngine] No microphone detected — skipping listen.")
            return None

        # Notify the UI that listening is about to begin
        if prompt_ui_callback:
            prompt_ui_callback("🎤  Robo is listening...")

        try:
            with sr.Microphone() as mic_source:

                # ── Step 1: Calibrate for room noise (0.5 sec) ────────
                # This runs every time because children play in noisy rooms.
                self.recognizer.adjust_for_ambient_noise(mic_source,
                                                         duration=0.5)

                # ── Step 2: Listen for up to listen_seconds seconds ───
                print(f"[VoiceEngine] Listening for {self.listen_seconds}s...")
                audio = self.recognizer.listen(
                    mic_source,
                    timeout=self.listen_seconds,       # max wait for speech start
                    phrase_time_limit=self.listen_seconds  # max speech length
                )

            # ── Step 3: Send audio to Google Web Speech API ───────────
            # Returns a plain text string, e.g. "lion" or "l"
            raw_text = self.recognizer.recognize_google(audio, language="en-US")

            # ── Step 4: Clean and return ──────────────────────────────
            # .lower()  → handles "Lion", "LION", "lion" all the same
            # .strip()  → removes accidental spaces at start/end
            clean_text = raw_text.lower().strip()

            print(f"[VoiceEngine] Heard: '{raw_text}'  →  cleaned: '{clean_text}'")
            return clean_text

        # ── Specific error handling — each case explained ─────────────

        except sr.WaitTimeoutError:
            # Child did not speak within the timeout window
            print("[VoiceEngine] Timeout — no speech detected.")
            return None

        except sr.UnknownValueError:
            # Google received audio but could not understand it
            # Common with children's voices — totally normal
            print("[VoiceEngine] Could not understand the audio.")
            return None

        except sr.RequestError as e:
            # Google API is unreachable — no internet or quota exceeded
            print(f"[VoiceEngine] Google API error: {e}")
            return None

        except OSError:
            # Microphone was disconnected mid-session
            self.mic_available = False
            print("[VoiceEngine] Microphone disconnected.")
            return None

    # ───────────────────────────────────────────────────────────
    #   PUBLIC METHOD 2 — VOICE OUTPUT (Robo speaks)
    # ───────────────────────────────────────────────────────────

    def speak(self, text: str):
        """
        Make Robo speak any text string.

        Runs in a BACKGROUND THREAD — the game screen stays live.
        Uses gTTS (natural voice) if available, else pyttsx3 (offline).

        Parameters
        ----------
        text : str
            What Robo should say. Use {name} placeholder and it will
            be replaced with the child's actual name automatically.

        Example
        -------
            robo_voice.speak("Well done {name}! L is for Lion!")
            # Robo says: "Well done Amir! L is for Lion!"
        """
        # Replace {name} with the child's real name
        text = text.replace("{name}", self.child_name)

        # Spawn a thread — do NOT call this from the main UI thread directly
        speech_thread = threading.Thread(
            target=self._speak_worker,
            args=(text,),
            daemon=True   # thread dies automatically if the game window closes
        )
        speech_thread.start()

    def _speak_worker(self, text: str):
        """
        Internal worker that runs inside the background thread.
        Tries gTTS first (better quality), falls back to pyttsx3.
        Uses a lock to prevent overlapping speech calls.
        """
        # If Robo is already speaking, wait briefly then speak
        # (prevents garbled audio from rapid correct-answer tapping)
        if not self._speech_lock.acquire(timeout=2.0):
            return  # skip this utterance — a newer one will follow

        try:
            if self.use_gtts:
                self._speak_with_gtts(text)
            else:
                self._speak_with_pyttsx3(text)
        finally:
            self._speech_lock.release()

    def _speak_with_gtts(self, text: str):
        """
        Speak using Google Text-to-Speech (warmer, more natural voice).
        Requires internet. Falls back to pyttsx3 on any failure.
        """
        try:
            # Generate speech audio and save to a temporary .mp3 file
            tts = gTTS(text=text, lang="en", slow=False)

            with tempfile.NamedTemporaryFile(suffix=".mp3",
                                             delete=False) as tmp:
                tmp_path = tmp.name

            tts.save(tmp_path)
            playsound.playsound(tmp_path)

            # Clean up temp file after playback
            os.remove(tmp_path)

        except Exception as e:
            print(f"[VoiceEngine] gTTS failed ({e}), using pyttsx3 fallback.")
            self._speak_with_pyttsx3(text)

    def _speak_with_pyttsx3(self, text: str):
        """
        Speak using pyttsx3 (offline, always available).
        Slightly robotic voice but no internet needed.
        """
        if not self._pyttsx3_ok:
            return
        try:
            self._pyttsx3_engine.say(text)
            self._pyttsx3_engine.runAndWait()
        except Exception as e:
            print(f"[VoiceEngine] pyttsx3 error: {e}")

    # ───────────────────────────────────────────────────────────
    #   PUBLIC CONVENIENCE METHODS — Pre-written Robo phrases
    # ───────────────────────────────────────────────────────────
    #
    #   These are the exact phrases other members call.
    #   All use {name} so Robo always says the child's real name.
    #   Member 1 (AI) calls speak_hint.
    #   Member 2 (UI) calls speak_question and speak_welcome.
    #   Member 3 (game logic) calls speak_praise and speak_wrong.
    #   Member 4 (score) calls speak_end_screen.
    #

    def speak_welcome(self):
        """Robo greets the child at the welcome screen."""
        self.speak(
            f"Hello {self.child_name}! I am Robo! "
            "Let's explore the jungle and learn letters together!"
        )

    def speak_question(self, animal_name: str):
        """
        Robo asks the question for the current animal.

        Parameters
        ----------
        animal_name : str  e.g. "Lion", "Bear", "Cat"
        """
        self.speak(
            f"What letter does {animal_name} start with? "
            "Tap the letter or say it out loud!"
        )

    def speak_praise(self, letter: str):
        """
        Robo celebrates a correct answer.
        Called by Member 3's game logic after a right answer.

        Parameters
        ----------
        letter : str  e.g. "L"
        """
        phrases = [
            f"YES! {letter} — well done, {{name}}! You are amazing!",
            f"Correct! {{name}}, you are so clever! {letter} is right!",
            f"Brilliant, {{name}}! {letter} — Robo is SO proud of you!",
            f"Fantastic! {letter} is the right answer! Keep going, {{name}}!",
        ]
        # Rotate through praise phrases to keep the child engaged
        import random
        self.speak(random.choice(phrases))

    def speak_wrong(self, letter: str):
        """
        Robo gently encourages after a wrong answer.
        NON-PUNITIVE — never sounds harsh or discouraging.
        Called by Member 3's game logic after a wrong answer.

        Parameters
        ----------
        letter : str  The CORRECT letter (not what child pressed)
        """
        self.speak(
            f"Oops! Good try, {{name}}! "
            f"This one starts with the letter {letter}. "
            "You can do it — try again!"
        )

    def speak_hint(self, letter: str, animal_name: str):
        """
        Robo gives a hint after 2 wrong answers on the same letter.
        Called by Member 1's AI module when mistake_count[letter] >= 2.

        Parameters
        ----------
        letter : str       e.g. "L"
        animal_name : str  e.g. "Lion"
        """
        self.speak(
            f"Here is a clue, {{name}}! "
            f"Listen carefully... {letter}... {letter}... "
            f"{letter} is for {animal_name}! "
            "Now tap the right letter!"
        )

    def speak_end_screen(self, stars: int, struggled_letters: list):
        """
        Robo summarises the session on the end screen.
        Called by Member 4's score module.

        Parameters
        ----------
        stars           : int   Number of stars earned (0–5)
        struggled_letters : list  e.g. ["B", "D", "F"] from mistake_count
        """
        star_phrase = "⭐" * stars if stars > 0 else ""
        end_text    = (
            f"Amazing work, {{name}}! You earned {stars} stars today! "
            f"{star_phrase} "
        )
        if struggled_letters:
            letters_str = ", ".join(struggled_letters)
            end_text += (
                f"Let's practise {letters_str} more next time. "
                "You are getting better every day!"
            )
        else:
            end_text += "You got every letter right! Robo is so happy!"

        self.speak(end_text)

    def speak_instruction(self):
        """Robo reads the instruction screen aloud for pre-readers."""
        self.speak(
            "Here is how to play! "
            "Robo will show you a jungle animal. "
            "Tap the letter the animal starts with, "
            "or say the letter out loud into the microphone. "
            "Ready? Let's go!"
        )


# ═══════════════════════════════════════════════════════════════
#   HELPER FUNCTION — answer matching
# ═══════════════════════════════════════════════════════════════

def match_answer(spoken_text: str, correct_letter: str) -> bool:
    """
    Check whether the child's spoken answer matches the correct letter.

    Called by Member 3's game_logic.py after listen() returns a string.
    Works for both single-letter answers ("l") and full word answers ("lion").

    Parameters
    ----------
    spoken_text    : str  What listen() returned — already lowercase + stripped
    correct_letter : str  The correct letter, e.g. "L" or "l"

    Returns
    -------
    bool  True if the answer is correct

    Examples
    --------
    match_answer("l",    "L")  → True   child said letter directly
    match_answer("lion", "L")  → True   child said the whole word
    match_answer("b",    "L")  → False  wrong letter
    match_answer("bear", "L")  → False  wrong animal
    """
    if not spoken_text:
        return False

    correct = correct_letter.lower().strip()
    spoken  = spoken_text.lower().strip()

    # Direct letter match: child said "l"
    if spoken == correct:
        return True

    # First-letter match: child said "lion" → first char is "l"
    if spoken and spoken[0] == correct:
        return True

    return False


# ═══════════════════════════════════════════════════════════════
#   MIC BUTTON HANDLER — connects to Member 2's UI button
# ═══════════════════════════════════════════════════════════════

def on_mic_button_pressed(voice_engine: VoiceEngine,
                          correct_letter: str,
                          on_correct_callback,
                          on_wrong_callback,
                          update_label_callback=None):
    """
    Full handler for when the child presses the microphone button.

    Member 2 connects this to the mic CTkButton's command parameter:
        mic_btn = ctk.CTkButton(
            ...,
            command=lambda: on_mic_button_pressed(
                robo_voice, current_letter,
                game.correct_answer, game.wrong_answer,
                status_label.configure
            )
        )

    Parameters
    ----------
    voice_engine         : VoiceEngine  The shared VoiceEngine instance
    correct_letter       : str          The right answer for this question
    on_correct_callback  : callable     Member 3's correct-answer function
    on_wrong_callback    : callable     Member 3's wrong-answer function
    update_label_callback: callable     Optional — updates a UI status label
    """

    def _run():
        # Step 1: Listen (this blocks inside its own thread — UI stays live)
        spoken = voice_engine.listen(
            prompt_ui_callback=update_label_callback
        )

        # Step 2: If nothing heard, update label and return quietly
        if spoken is None:
            if update_label_callback:
                update_label_callback({"text": "Didn't catch that — try again! 🎤"})
            return

        # Step 3: Match the spoken word against the correct letter
        if match_answer(spoken, correct_letter):
            on_correct_callback()   # Member 3's function → triggers green flash, score++
        else:
            on_wrong_callback()     # Member 3's function → triggers soft sound, retry

    # Run the whole flow in a background thread so the button stays responsive
    threading.Thread(target=_run, daemon=True).start()


# ═══════════════════════════════════════════════════════════════
#   QUICK TEST — run this file directly to test your mic + TTS
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 55)
    print("  Robo's Jungle ABC — VoiceEngine Self-Test")
    print("=" * 55)

    # --- Test 1: Create engine ---
    print("\n[TEST 1] Initialising VoiceEngine...")
    engine = VoiceEngine(child_name="Amir", use_gtts=False)
    print(f"  Mic available : {engine.mic_available}")
    print(f"  pyttsx3 OK    : {engine._pyttsx3_ok}")
    print(f"  gTTS ready    : {engine.use_gtts}")

    # --- Test 2: Robo speaks ---
    print("\n[TEST 2] Robo speaks the welcome phrase...")
    engine.speak_welcome()
    time.sleep(4)   # wait for speech to finish before next test

    # --- Test 3: Robo asks a question ---
    print("\n[TEST 3] Robo asks a question about Lion...")
    engine.speak_question("Lion")
    time.sleep(4)

    # --- Test 4: Listen for answer ---
    print("\n[TEST 4] Listening test — say a letter or animal name...")
    result = engine.listen()
    print(f"  You said: '{result}'")

    if result is not None:
        is_correct = match_answer(result, "L")
        print(f"  Correct for 'L'? → {is_correct}")
        if is_correct:
            engine.speak_praise("L")
        else:
            engine.speak_wrong("L")
        time.sleep(4)

    # --- Test 5: Hint ---
    print("\n[TEST 5] Hint after 2 wrong tries...")
    engine.speak_hint("L", "Lion")
    time.sleep(5)

    # --- Test 6: End screen ---
    print("\n[TEST 6] End screen with 4 stars, struggled B and D...")
    engine.speak_end_screen(stars=4, struggled_letters=["B", "D"])
    time.sleep(6)

    print("\n[DONE] All tests complete. Voice engine is ready.")
    print("=" * 55)
