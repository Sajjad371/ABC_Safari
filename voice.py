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

# Global lock to serialize speech and prevent overlapping background voice tasks
_voice_lock = threading.Lock()

# Strictly set to the onboarding instruction text specified
WELCOME_PHRASES = [
    "Hi! Welcome to Safari Jungle Game. Nice to have you! Write your name and choose your difficulty level to start the game."
]

GAME_START_PHRASES = [
    "Let us find some animals, {name}! Are you ready?",
    "Buckle up, {name}! Our safari adventure is starting! Let's go!",
    "Alright, {name}! Let's head into the jungle and find some cool animals!",
    "Here we go, {name}! Keep your eyes open for wild animals! Let's search!",
    "Are you ready to explore, {name}? Let's start finding letters in the wild!",
]

QUESTION_PHRASES = [
    "What letter does this animal start with?",
    "Which letter makes the first sound of that animal?",
    "Can you find the starting letter for this animal?",
    "What letter does this beautiful animal begin with?",
    "Help me find the first letter of this animal!",
]

GAME_END_PHRASES = [
    "Amazing adventure today, {name}! You did fantastic!",
    "Wow, {name}! What a spectacular safari trip! You did great!",
    "That was an incredible journey, {name}! You're an expert explorer!",
    "Fantastic job, {name}! The jungle animals are so happy you visited!",
    "Hurrah, {name}! You completed the ABC Safari! You're a true champion!",
]

WELCOME_BACK_PHRASES = [
    "Welcome back, {name}! Ready for round 2?",
    "You came back for more, {name}! Let's go!",
    "Another round, {name}? I love your spirit!",
    "Great to see you again, {name}! Let's find more jungle animals!",
    "Welcome back, explorer {name}! Our safari is waiting!",
    "Awesome, {name} is back! Let's start the adventure!",
    "Hello again, {name}? Ready for some more alphabet fun?",
    "You're back, {name}! Let's see if we can get a perfect score!",
    "I missed you, {name}! Let's jump back into the safari!",
    "Welcome back to the jungle, {name}! Let's track some letters!",
    "Fantastic! {name} has returned for another wild ride!",
    "Ready for another round of ABC Safari, {name}? Let's do it!",
    "Welcome back, {name}! Let's see what animals we can find today!"
]

HINT_PHRASES = [
    "The answer is {letter}! {animal} starts with {letter}!",
    "Look closely! {animal} begins with the letter {letter}!",
    "Need help? {animal} starts with the sound of {letter}!",
    "I think it starts with {letter}, just like in {animal}!",
    "Try pressing {letter}! {animal} starts with {letter}!",
    "Here is a clue: {animal} matches the letter {letter}!",
    "Psst! The starting letter of {animal} is {letter}!",
    "Don't worry, explorer! {animal} starts with {letter}!",
    "The first letter of {animal} is {letter}! Go ahead and tap it!",
    "Let's look for {letter}! {animal} starts with {letter}!",
    "Hear the sound: {letter} is for {animal}!"
]

ROBO_LINES = {
    "welcome":          "Hi! Welcome to Safari Jungle Game. Nice to have you! Write your name and choose your difficulty level to start the game.",
    "ask_name":         "What is your name, explorer?",
    "game_start":       "Let us find some animals, {name}! Are you ready?",
    "question":         "What letter does this animal start with?",
    "game_end":         "Amazing adventure today, {name}!",
    "hint":             "The answer is {letter}! {animal} starts with {letter}!"
}

WRONG_PHRASES = [
    "Hmm! Try again, {name}, you can do it!",
    "Not quite! Have another go, explorer!",
    "Look closely at the card, {name}! Try picking another option!",
    "Jungle explorers never give up! Let's choose a different letter!",
    "No worries, {name}! Try one more time!",
    "Oh, so close! Give it another shot, explorer!",
    "Don't worry, {name}! Let's try another one!",
    "Almost there! Try again and you will get it!",
    "Mistakes help us learn! Try another letter, {name}!"
]

CORRECT_PHRASES = [
    "Amazing, {name}! You got it!",
    "Fantastic! You are so smart, {name}!",
    "Wonderful! Keep going, explorer!",
    "Brilliant! You are a true jungle champion!",
    "Awesome job, {name}! You found it!",
    "Great work, {name}! That is the correct answer!",
    "You got it, explorer! Keep up the good work!",
    "Superb! You are doing great, {name}!",
    "Correct! You are becoming a master explorer!",
    "Spot on, {name}! That is absolutely right!"
]

# 21 distinct loud male spoken lines for speech timeouts/errors
MIC_FAIL_PHRASES = [
    "I cannot hear you, please repeat!",
    "Speak up explorer, say it again!",
    "Could you say that one more time? I didn't catch it!",
    "Jungle noise is too loud! Please repeat the letter clearly!",
    "I did not hear any answer! Try speaking closer to the microphone!",
    "Please say it again, explorer! I'm listening closely!",
    "Hmm, I missed that completely. Can you repeat it?",
    "Speak clearly and loudly so I can hear you!",
    "My monkey ears missed that! Repeat it once more!",
    "Say it again! Which letter is it?",
    "Could you speak up a bit and repeat the letter?",
    "I didn't quite catch that. Try saying it one more time!",
    "I'm listening, but I didn't hear anything! Try again!",
    "Please repeat your answer! Speak right into the mic!",
    "I cannot hear your voice! Try speaking louder!",
    "Let's try that again! Say the letter loud and proud!",
    "Speak up! The animals are waiting for your answer!",
    "Did you say something? Please repeat that letter!",
    "I need you to speak louder, explorer! Say it again!",
    "Oops! I didn't catch that. Please repeat your answer!",
    "Loud and clear, explorer! Repeat the letter for me!"
]

MIC_CORRECT_PHRASES = [
    "Incredible! I heard your voice loud and clear, and it is absolutely correct!",
    "Outstanding! Your voice command was perfect, and that is the right starting letter!",
    "Fantastic speech, explorer! You pronounced it beautifully and got it correct!",
    "Spot on! I heard you say it, and you are 100 percent correct!",
    "Marvellous job! Your voice recognition was a total success, well done!",
    "Brilliant! I captured your answer perfectly, and you nailed it!",
    "Excellent pronunciation! That is indeed the correct starting letter!",
    "Bingo! Your spoken letter matches the animal perfectly! Great job!",
    "Superb! You said it beautifully and got the answer right!",
    "You speak like a true scientist, explorer! That is completely correct!"
]

def robo_speak_sync(text):
    """Reinforced voice engine: Selects a strong, bold male voice (e.g. David)."""
    if not PYTTSX3_AVAILABLE:
        print(f"[Robo Alternative Engine]: {text}")
        return
    with _voice_lock:
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            selected_voice_id = None
            
            # Explicitly find microsoft david or male voice
            for v in voices:
                if "david" in v.name.lower() or "male" in str(v.gender).lower():
                    selected_voice_id = v.id
                    break
            if not selected_voice_id and len(voices) > 0:
                selected_voice_id = voices[0].id

            if selected_voice_id:
                engine.setProperty('voice', selected_voice_id)
            
            engine.setProperty("rate", 150) # perfect scannable speed for kids
            engine.setProperty("volume", 1.0) # force volume to 1.0 (loudest)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Voice pipeline error encounter: {e}")

def get_random_welcome():
    return random.choice(WELCOME_PHRASES)

def robo_say(line_key, name="", letter="", animal="", custom_text=None):
    if custom_text:
        text = custom_text
    else:
        if line_key == "welcome":
            text = random.choice(WELCOME_PHRASES)
        elif line_key == "game_start":
            text = random.choice(GAME_START_PHRASES)
        elif line_key == "question":
            text = random.choice(QUESTION_PHRASES)
        elif line_key == "game_end":
            text = random.choice(GAME_END_PHRASES)
        elif line_key == "wrong_random":
            text = random.choice(WRONG_PHRASES)
        elif line_key == "welcome_back":
            text = random.choice(WELCOME_BACK_PHRASES)
        elif line_key == "hint":
            text = random.choice(HINT_PHRASES)
        elif line_key == "mic_fail":
            text = random.choice(MIC_FAIL_PHRASES)
        elif line_key == "mic_correct":
            text = random.choice(MIC_CORRECT_PHRASES)
        else:
            text = ROBO_LINES.get(line_key, "")
    
    filled_text = text.replace("{name}", str(name)).replace("{letter}", str(letter)).replace("{animal}", str(animal))
    print(f"[Robo Speech Out]: {filled_text}")
    robo_speak_sync(filled_text)

def robo_say_correct(name="", count=1):
    base_phrase = random.choice(CORRECT_PHRASES)
    filled_text = base_phrase.replace("{name}", str(name))
    print(f"[Robo Speech Out]: {filled_text}")
    robo_speak_sync(filled_text)

PHONETIC_LETTERS = {
    "ay": "A", "hey": "A", "a": "A", "aye": "A",
    "bee": "B", "be": "B", "b": "B", "bi": "B",
    "see": "C", "sea": "C", "c": "C", "si": "C",
    "dee": "D", "de": "D", "d": "D", "di": "D",
    "ee": "E", "e": "E",
    "eff": "F", "ef": "F", "f": "F",
    "gee": "G", "ji": "G", "g": "G",
    "aitch": "H", "eight": "H", "h": "H",
    "eye": "I", "i": "I",
    "jay": "J", "j": "J",
    "kay": "K", "k": "K", "kai": "K",
    "el": "L", "ell": "L", "l": "L",
    "em": "M", "m": "M",
    "en": "N", "and": "N", "n": "N",
    "oh": "O", "ow": "O", "o": "O",
    "pee": "P", "pea": "P", "p": "P",
    "cue": "Q", "queue": "Q", "q": "Q",
    "ar": "R", "are": "R", "r": "R",
    "ess": "S", "es": "S", "s": "S",
    "tee": "T", "tea": "T", "t": "T",
    "you": "U", "u": "U",
    "vee": "V", "we": "V", "v": "V",
    "double you": "W", "w": "W", "wee": "W",
    "ex": "X", "x": "X", "eks": "X",
    "why": "Y", "y": "Y", "wai": "Y",
    "zed": "Z", "zee": "Z", "z": "Z"
}

def listen_for_letter(timeout=3):
    if not SR_AVAILABLE: 
        raise ImportError("speech_recognition library not available")
    rec = sr.Recognizer()
    rec.energy_threshold = 300
    rec.pause_threshold = 0.8
    
    try:
        with sr.Microphone() as source:
            # Calibrate noise faster (0.2s instead of 0.5s)
            rec.adjust_for_ambient_noise(source, duration=0.2)
            try:
                # Snappy timeouts for phrase listening to prevent long waits
                audio = rec.listen(source, timeout=timeout, phrase_time_limit=2)
            except sr.WaitTimeoutError:
                raise ValueError("No sound detected! Speak closer/louder")
        
        spoken_str = rec.recognize_google(audio).strip().lower()
        print(f"[Speech Recog Result]: {spoken_str}")
        if spoken_str:
            try:
                from data.questions import QUESTIONS
                for q in QUESTIONS:
                    if spoken_str == q["animal"].lower():
                        return q["letter"]
                for w in spoken_str.split():
                    for q in QUESTIONS:
                        if w == q["animal"].lower():
                            return q["letter"]
            except Exception as ex:
                print(f"Error checking animal name matching: {ex}")

            if spoken_str in PHONETIC_LETTERS:
                return PHONETIC_LETTERS[spoken_str]
                
            words = spoken_str.split()
            for w in words:
                if w in PHONETIC_LETTERS:
                    return PHONETIC_LETTERS[w]
                if len(w) == 1 and w.isalpha():
                    return w.upper()
            
            return spoken_str[0].upper()
    except sr.UnknownValueError:
        raise ValueError("Could not understand! Speak closer/louder")
    except sr.RequestError:
        raise ConnectionError("Google Speech API offline. Check internet")
    return None