import pygame
import random
from data.questions import QUESTIONS

def load_question(letter):
    for q in QUESTIONS:
        if q["letter"] == letter.upper():
            return q
    return None

def generate_choices(correct_letter):
    all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    wrong = [l for l in all_letters if l != correct_letter.upper()]
    three_wrong = random.sample(wrong, 3)
    choices = three_wrong + [correct_letter.upper()]
    random.shuffle(choices)
    return choices

def check_answer(chosen, correct):
    return chosen.upper() == correct.upper()

def play_correct_sound():
    try:
        pygame.mixer.init()
        pygame.mixer.Sound("assets/sounds/correct.wav").play()
    except:
        print("correct sound played")

def play_wrong_sound():
    try:
        pygame.mixer.init()
        pygame.mixer.Sound("assets/sounds/wrong.wav").play()
    except:
        print("wrong sound played")

def play_animal_sound(letter):
    q = load_question(letter)
    if q:
        try:
            pygame.mixer.init()
            pygame.mixer.Sound(q["sound"]).play()
        except:
            print(f"animal sound played for {letter}")

if __name__ == "__main__":
    q = load_question("L")
    print(q)
    choices = generate_choices("L")
    print(choices)
    result = check_answer("L", "L")
    print(result)

