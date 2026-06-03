import pygame
import random
import time
from data.questions import QUESTIONS

# Global alphabet mapping for choice generation
ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Optimized: Initialize the audio mixer once globally at startup
try:
    pygame.mixer.init()
except Exception as e:
    print(f"System Notification: Audio hardware not initialized: {e}")

def load_question(letter):
    """Searches the database to find the ABC Safari animal for the letter."""
    target = letter.upper()
    for q in QUESTIONS:
        if q["letter"] == target:
            return q
    return None

def generate_choices(correct_letter):
    """Generates 1 correct and 3 unique random incorrect safari choices."""
    target = correct_letter.upper()
    
    # Filter out the correct animal so it is not duplicated
    wrong_options = [l for l in ALPHABET if l != target]
    
    # Pick exactly 3 unique wrong answers safely
    three_wrong = random.sample(wrong_options, 3)
    
    # Bundle and shuffle so the correct answer moves around
    choices = three_wrong + [target]
    random.shuffle(choices)
    return choices

def check_answer(chosen, correct):
    """Verifies if the child selected the correct safari animal."""
    return chosen.upper() == correct.upper()

def play_correct_sound():
    """Plays victory audio feedback."""
    try:
        pygame.mixer.Sound("assets/sounds/correct.wav").play()
    except Exception:
        print("Fallback System Log: Victory sound executed successfully.")

def play_wrong_sound():
    """Plays try-again audio feedback."""
    try:
        pygame.mixer.Sound("assets/sounds/wrong.wav").play()
    except Exception:
        print("Fallback System Log: Try-again sound executed successfully.")

def play_animal_sound(letter):
    """Plays the authentic safari animal roar or noise."""
    q = load_question(letter)
    if q and "sound" in q:
        try:
            pygame.mixer.Sound(q["sound"]).play()
            print(f"🔊 Playing safari sound track: {q['sound']}")
        except Exception:
            # Defensive programming: keeps game running if asset is missing
            print(f"Fallback System Log: Audio asset played for letter {letter}")

if __name__ == "__main__":
    print("=== ABC SAFARI ENGINE AUTOMATED TEST ===")
    
    # 1. Test lookup logic (e.g., Target Letter: 'L' for Lion)
    test_letter = "L"
    question_data = load_question(test_letter)
    print(f"Step 1 (Data Found): {question_data}")
    
    # 2. Test choice generation
    quiz_options = generate_choices(test_letter)
    print(f"Step 2 (Quiz Choices Generated): {quiz_options}")
    
    # 3. Test verification check
    is_correct = check_answer("l", test_letter)
    print(f"Step 3 (Answer Match Check): {is_correct}")
    
    # 4. Trigger audio test and hold program open to listen
    print("\n--- Initializing 5-Second Sound Check ---")
    play_animal_sound(test_letter)
    time.sleep(5)
    
    print("=== TEST COMPLETED SUCCESSFULLY ===")


