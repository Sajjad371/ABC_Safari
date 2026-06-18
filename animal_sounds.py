import os
import pygame

def play_animal_sound(animal_name):
    # Search for sound files in assets/sounds/animals/
    # Supports both lowercase .wav and potential case variations
    path = f"assets/sounds/animals/{animal_name.lower()}.wav"
    if os.path.exists(path):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.Sound(path).play()
        except Exception as e:
            print(f"Error playing animal sound {animal_name}: {e}")
    else:
        print(f"Animal sound not found for {animal_name} at {path}")
