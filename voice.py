# -*- coding: utf-8 -*-
"""
ABC Safari - Voice Engine
File: voice.py
"""

import os, threading, time, random, urllib.request

def _has_internet():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=2)
        return True
    except Exception: return False

INTERNET_AVAILABLE = _has_internet()

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

ROBO_LINES = {
    "welcome":          "Hi! I am Robo! Your jungle guide today!",
    "ask_name":         "What is your name, explorer?",
    "game_start":       "Let us find some animals, {name}! Are you ready?",
    "question":         "What letter does this animal start with?",
    "game_end":         "Amazing adventure today, {name}!",
}

# Instruction 4: Broad pool of motivational expressions for wrong-answer selections
WRONG_PHRASES = [
    "Hmm! Try again, {name}, you can do it!",
    "Not quite! Have another go, explorer!",
    "Look closely at the card, {name}! Try picking another option!",
    "Jungle explorers never give up! Let's choose a different letter!",
]

CORRECT_PHRASES = [
    "Amazing, {name}! You got it!",
    "Fantastic! You are so smart, {name}!",
    "Wonderful! Keep going, explorer!",
    "Brilliant! You are a true jungle champion!",
]

def robo_speak_sync(text):
    """Reinforced voice engine: Prevents background tasks from cutting off early."""
    if not PYTTSX3_AVAILABLE:
        print(f"[Robo Alternative Engine]: {text}")
        return
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        # Explicit shutdown clears background speech buffers safely
        engine.stop()
    except Exception as e:
        print(f"Voice pipeline error encounter: {e}")

def robo_say(line_key, name="", custom_text=None):
    if custom_text:
        text = custom_text
    else:
        text = ROBO_LINES.get(line_key, "")
        if line_key == "wrong_random":
            text = random.choice(WRONG_PHRASES)
    
    filled_text = text.replace("{name}", str(name))
    print(f"[Robo Speech Out]: {filled_text}")
    robo_speak_sync(filled_text)

def robo_say_correct(name="", count=1):
    base_phrase = random.choice(CORRECT_PHRASES)
    filled_text = base_phrase.replace("{name}", str(name))
    print(f"[Robo Speech Out]: {filled_text}")
    robo_speak_sync(filled_text)

def listen_for_letter(timeout=5):
    if not SR_AVAILABLE: 
        raise ImportError("speech_recognition library not available")
    rec = sr.Recognizer()
    rec.energy_threshold = 300 
    rec.pause_threshold = 0.4
    
    # Check for microphone availability; with sr.Microphone() raises OSError if missing
    with sr.Microphone() as source:
        audio = rec.listen(source, timeout=timeout, phrase_time_limit=3)
    
    try:
        spoken_str = rec.recognize_google(audio).strip().lower()
        print(f"[Speech Recog Result]: {spoken_str}")
        if spoken_str:
            words = spoken_str.split()
            for w in words:
                if len(w) == 1 and w.isalpha():
                    return w.upper()
            return spoken_str[0].upper()
    except sr.UnknownValueError:
        raise ValueError("Could not understand! Speak closer/louder")
    except sr.RequestError:
        raise ConnectionError("Google Speech API offline. Check internet")
    return None