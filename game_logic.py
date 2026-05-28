import random
import os
import pygame
from data.questions import QUESTIONS

# Initialize the pygame sound mixer system safely
try:
    pygame.mixer.init()
except Exception:
    print("⚠️ Warning: Audio hardware not detected. Sounds will print instead of playing.")

def load_question(letter):
    """Finds and returns the question dictionary for that letter."""
    for question in QUESTIONS:
        if question["letter"] == letter.upper():
            return question
    return None

def generate_choices(correct_letter):
    """Returns a list of 4 letters: 1 correct + 3 random wrong, shuffled."""
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    correct_letter = correct_letter.upper()
    
    if correct_letter in alphabet:
        alphabet.remove(correct_letter)
        
    wrong_choices = random.sample(alphabet, 3)
    choices = wrong_choices + [correct_letter]
    random.shuffle(choices)
    return choices

def check_answer(chosen, correct):
    """Returns True if match, False if not."""
    return str(chosen).upper() == str(correct).upper()

def play_correct_sound():
    """Uses pygame.mixer to play your actual local correct ding file."""
    sound_path = os.path.join("assets", "sounds", "animals", "correct ding.mp3")
    if os.path.exists(sound_path):
        pygame.mixer.Sound(sound_path).play()
    else:
        print("🔊 [Sound] Ding! Correct!")

def play_wrong_sound():
    """Uses pygame.mixer to play your actual local wrong buzzer file."""
    sound_path = os.path.join("assets", "sounds", "animals", "wrong buzzer.mp3")
    if os.path.exists(sound_path):
        pygame.mixer.Sound(sound_path).play()
    else:
        print("🔊 [Sound] Buzz! Wrong answer.")

def play_animal_sound(letter):
    """Plays the animal sound file for that letter (used for hints)."""
    question_data = load_question(letter)
    if question_data and "sound" in question_data:
        sound_path = question_data["sound"]
        if os.path.exists(sound_path):
            pygame.mixer.Sound(sound_path).play()
        else:
            print(f"🔊 [Sound] Simulated Roar/Chirp for {question_data['animal']}!")
    else:
        print(f"❌ Error: Sound path not configured for letter {letter}")

if __name__ == '__main__':
    # --- SECTION 1: STANDALONE LOGIC TESTS ---
    print("--- Running Automated Logic Diagnostics ---")
    q = load_question('L')
    print(f"Loaded Dictionary: {q}")
    
    choices = generate_choices('L')
    print(f"Generated Choices List: {choices}")
    
    result = check_answer('L', 'L')
    print(f"Evaluation Validation Check: {result}")  # Expected: True
    print("-------------------------------------------\n")

    # --- SECTION 2: 4-TO-7-YEAR-OLD GAME LOOP ---
    print("🐾 ✨ WELCOME TO THE ABC SAFARI GAME! ✨ 🐾")
    print("(Parents/Teachers: Type 'quit' to close the game anytime.)")
    print("=========================================================")
    
    while True:
        # 1. Grab a completely random animal item from our list
        current_q = random.choice(QUESTIONS)
        current_letter = current_q['letter']
        
        # 2. Get the shuffled options list
        round_choices = generate_choices(current_letter)
        
        # 3. Find which menu row index matching option contains the target letter
        correct_number = round_choices.index(current_letter) + 1
        
        print(f"\n🐯 Can you find the starting letter for: **{current_q['animal']}**?")
        print(f"1️⃣  👉  [ {round_choices[0]} ]")
        print(f"2️⃣  👉  [ {round_choices[1]} ]")
        print(f"3️⃣  👉  [ {round_choices[2]} ]")
        print(f"4️⃣  👉  [ {round_choices[3]} ]")
        print("")
        
        # Ask for help sound right away to guide the child phonetically
        play_animal_sound(current_letter)
        
        user_input = input("Press button 1, 2, 3, or 4: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nGoodbye little explorer! Thanks for touring the Safari! 👋🐾")
            break
            
        if user_input == str(correct_number):
            print("\n⭐️ 🎈 YOU DID IT! 🎈 ⭐️")
            print(f"🎉 Hooray! {current_q['hint']}")
            print(f"🖼️  [Showing Image]: {current_q['image']}")
            play_correct_sound()
            print("\n✨ Ready for the next one? ✨")
            print("=========================================")
        else:
            print("\nNice try! Let's check our map... 🗺️")
            print(f"💡 Hint: {current_q['hint']}")
            play_wrong_sound()
            print("\nTry pressing another number button! 👇")
            print("=========================================")
