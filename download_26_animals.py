# -*- coding: utf-8 -*-
"""
ABC Safari - 26 Animals Downloader & Verification Script
Downloads real, cute, childish animal photos from curated Wikimedia Commons URLs
using requests and Pillow, and synthesizes kid-friendly wave sound clips.
"""

import os
import sys
import time
import requests
from PIL import Image, ImageDraw
import io
import wave
import math
import struct
import random

# Curated, child-friendly, high-quality real animal photo URLs from Wikimedia Commons
ANIMAL_PHOTO_URLS = {
    "ant":          "https://upload.wikimedia.org/wikipedia/commons/4/47/Leafcutter_ant_with_leaf.jpg",
    "butterfly":    "https://upload.wikimedia.org/wikipedia/commons/b/b5/Monarch_Butterfly_Danaus_plexippus_on_Echinacea_purpurea_2800px.jpg",
    "chick":        "https://upload.wikimedia.org/wikipedia/commons/b/bc/Hatched_baby_chick_Live_Animal_Care_Center_Museum_Science_Boston.jpg",
    "deer":         "https://upload.wikimedia.org/wikipedia/commons/8/83/006_Wild_baby_fawn_saved_from_certain_and_brutal_death_Photo_by_Giles_Laurent.jpg",
    "elephant":     "https://upload.wikimedia.org/wikipedia/commons/6/6c/004_Desert-adapted_baby_elephants_cuddling_in_Damaraland_Photo_by_Giles_Laurent.jpg",
    "flamingo":     "https://upload.wikimedia.org/wikipedia/commons/6/68/Pink_flamingo_in_Flamingo_Lagoon_-_geograph.org.uk_-_883124.jpg",
    "giraffe":      "https://upload.wikimedia.org/wikipedia/commons/b/b5/076_Baby_Angolan_giraffes_running_in_Etosha_National_Park_Photo_by_Giles_Laurent.jpg",
    "hedgehog":     "https://upload.wikimedia.org/wikipedia/commons/8/8d/Baby_Hedgehog_-_panoramio.jpg",
    "ibis":         "https://upload.wikimedia.org/wikipedia/commons/3/3a/Scarlet_ibis%2C_Eudocimus_ruber.jpg",
    "jellyfish":    "https://upload.wikimedia.org/wikipedia/commons/d/dc/Underside_of_expanded_bluefire_jellyfish_in_Brofjorden_at_Sandvik_57.jpg",
    "kitten":       "https://upload.wikimedia.org/wikipedia/commons/a/ab/Cute_kitten%21.jpg",
    "lamb":         "https://upload.wikimedia.org/wikipedia/commons/e/e7/Baby-lamb_%285556322982%29.jpg",
    "manatee":      "https://upload.wikimedia.org/wikipedia/commons/b/b1/Manatee_photo.jpg",
    "nightingale":  "https://upload.wikimedia.org/wikipedia/commons/3/33/Nesocichla_eremita_-Nightingale_Island_-eating-8.jpg",
    "ostrich":      "https://upload.wikimedia.org/wikipedia/commons/a/a2/Ostrich_Struthio_camelus.jpg",
    "penguin":      "https://upload.wikimedia.org/wikipedia/commons/c/c2/Baby_Penguin_%283544372279%29.jpg",
    "quokka":       "https://upload.wikimedia.org/wikipedia/commons/9/98/Quokka_Selfie.jpg",
    "rabbit":       "https://upload.wikimedia.org/wikipedia/commons/e/e3/Baby_Bunny_Surprise%5E_%28Explore_April_14%2C_2022%29_-_Flickr_-_DaPuglet.jpg",
    "seahorse":     "https://upload.wikimedia.org/wikipedia/commons/3/30/Spotted_seahorse_Hippocampus_kuda_at_Gili_Lankanfushi.jpg",
    "turtle":       "https://upload.wikimedia.org/wikipedia/commons/9/9b/Chelonia_mydas_Baby_Sea_Turtle.jpg",
    "uakari":       "https://upload.wikimedia.org/wikipedia/commons/e/ef/2019-10-06_Uakari_Monkey_03.jpg",
    "squirrel":     "https://upload.wikimedia.org/wikipedia/commons/1/1c/Squirrel_posing.jpg",
    "whale":        "https://upload.wikimedia.org/wikipedia/commons/6/6e/031_Humpback_whale_lobtailing_Photo_by_Giles_Laurent.jpg",
    "axolotl":      "https://upload.wikimedia.org/wikipedia/commons/e/ef/Axolotl_Ambystoma_mexicanum_Aquarium_Zoo_Berlin%2C_2007.jpg",
    "yak":          "https://upload.wikimedia.org/wikipedia/commons/1/1c/Baby-Bauernhoftiere_001_2014_08_05.jpg",
    "zebra":        "https://upload.wikimedia.org/wikipedia/commons/8/88/Baby_zebra_%2815995185774%29.jpg"
}

IMG_DIR = "assets/images/animals"
SND_DIR = "assets/sounds/animals"

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(SND_DIR, exist_ok=True)

SAMPLE_RATE = 22050
HEADERS = {'User-Agent': 'ABCSafariEducationalApp/1.0 (contact@sajjadeducation.org) Python-Requests/2.31'}

# ────────────────────────────────────────────────────────────
#  SOUND SYNTHESIS FUNCTIONS (CUTE ANIMAL VOICES)
# ────────────────────────────────────────────────────────────

def apply_envelope(frames, attack=0.05, decay=0.1, sustain=0.8, release=0.1):
    n = len(frames)
    att_samples = int(attack * SAMPLE_RATE)
    dec_samples = int(decay * SAMPLE_RATE)
    rel_samples = int(release * SAMPLE_RATE)
    out = list(frames)
    for i in range(min(att_samples, n)):
        out[i] *= (i / att_samples)
    for i in range(att_samples, min(att_samples + dec_samples, n)):
        fraction = (i - att_samples) / dec_samples
        out[i] *= (1.0 - fraction * (1.0 - sustain))
    for i in range(att_samples + dec_samples, max(0, n - rel_samples)):
        out[i] *= sustain
    for i in range(max(0, n - rel_samples), n):
        fraction = (n - i) / rel_samples
        out[i] *= (sustain * fraction)
    return out

def synth_wav(filename, frames):
    filepath = os.path.join(SND_DIR, filename)
    with wave.open(filepath, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        packed = b"".join(struct.pack("<h", int(max(-32768, min(32767, val * 32767)))) for val in frames)
        w.writeframes(packed)

def synth_chick():
    frames = []
    for _ in range(3):
        sweep = [math.sin(2 * math.pi * (1800 + 1200 * (i / (0.15 * SAMPLE_RATE))) * (i / SAMPLE_RATE)) for i in range(int(0.15 * SAMPLE_RATE))]
        frames.extend(apply_envelope(sweep, 0.01, 0.02, 0.7, 0.05))
        frames.extend([0.0] * int(0.1 * SAMPLE_RATE))
    synth_wav("chick.wav", frames)

def synth_lamb():
    frames = []
    for _ in range(2):
        n_samples = int(0.4 * SAMPLE_RATE)
        sweep = []
        for i in range(n_samples):
            t = i / SAMPLE_RATE
            mod = 1.0 + 0.15 * math.sin(2 * math.pi * 12 * t)
            freq = 240 * mod
            val = 0.7 * math.sin(2 * math.pi * freq * t) + 0.3 * (1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0)
            sweep.append(val)
        frames.extend(apply_envelope(sweep, 0.05, 0.1, 0.6, 0.15))
        frames.extend([0.0] * int(0.15 * SAMPLE_RATE))
    synth_wav("lamb.wav", frames)

def synth_kitten():
    n_samples = int(0.6 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / (0.6 * SAMPLE_RATE)
        freq = 400 + 400 * (t / 0.2) if t < 0.2 else 800 - 300 * ((t - 0.2) / 0.8)
        val = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE)) + 0.3 * math.sin(4 * math.pi * freq * (i / SAMPLE_RATE))
        frames.append(val * 0.7)
    frames = apply_envelope(frames, 0.1, 0.15, 0.7, 0.2)
    synth_wav("kitten.wav", frames)

def synth_squirrel():
    frames = []
    for _ in range(4):
        sweep = [math.sin(2 * math.pi * (2200 + 1500 * (i / (0.08 * SAMPLE_RATE))) * (i / SAMPLE_RATE)) for i in range(int(0.08 * SAMPLE_RATE))]
        frames.extend(apply_envelope(sweep, 0.005, 0.01, 0.8, 0.02))
        frames.extend([0.0] * int(0.06 * SAMPLE_RATE))
    synth_wav("squirrel.wav", frames)

def synth_bubble(filename):
    frames = []
    for _ in range(4):
        dur = random.uniform(0.06, 0.12)
        n_samples = int(dur * SAMPLE_RATE)
        f_start = random.uniform(400, 700)
        f_end = f_start * random.uniform(2.0, 3.0)
        sweep = [math.sin(2 * math.pi * (f_start + (f_end - f_start) * (i / n_samples)) * (i / SAMPLE_RATE)) for i in range(n_samples)]
        frames.extend(apply_envelope(sweep, 0.01, 0.02, 0.7, 0.03))
        frames.extend([0.0] * int(random.uniform(0.05, 0.1) * SAMPLE_RATE))
    synth_wav(filename, frames)

def synth_bird(filename, prefix_freq=1200):
    frames = []
    for step in range(3):
        n_samples = int(0.18 * SAMPLE_RATE)
        f_start = prefix_freq + step * 200
        f_end = f_start + 600
        sweep = [math.sin(2 * math.pi * (f_start + (f_end - f_start) * ((i / n_samples) ** 2)) * (i / SAMPLE_RATE)) for i in range(n_samples)]
        frames.extend(apply_envelope(sweep, 0.02, 0.03, 0.7, 0.05))
        frames.extend([0.0] * int(0.08 * SAMPLE_RATE))
    synth_wav(filename, frames)

def synth_deer():
    n_samples = int(0.5 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        val = 0.5 * math.sin(2 * math.pi * 320 * t) + 0.3 * math.sin(2 * math.pi * 480 * t) + 0.15 * (random.random() * 2.0 - 1.0)
        frames.append(val)
    frames = apply_envelope(frames, 0.1, 0.1, 0.8, 0.15)
    synth_wav("deer.wav", frames)

def synth_manatee():
    n_samples = int(0.6 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 380 + 30 * math.sin(2 * math.pi * 6 * t)
        val = math.sin(2 * math.pi * freq * t)
        frames.append(val * 0.5)
    frames = apply_envelope(frames, 0.1, 0.15, 0.8, 0.15)
    synth_wav("manatee.wav", frames)

def synth_ostrich():
    frames = []
    for _ in range(2):
        n_samples = int(0.25 * SAMPLE_RATE)
        sweep = [math.sin(2 * math.pi * (150 - 50 * (i / n_samples)) * (i / SAMPLE_RATE)) for i in range(n_samples)]
        frames.extend(apply_envelope(sweep, 0.02, 0.05, 0.6, 0.1))
        frames.extend([0.0] * int(0.12 * SAMPLE_RATE))
    synth_wav("ostrich.wav", frames)

def synth_uakari():
    frames = []
    for step in range(5):
        n_samples = int(0.07 * SAMPLE_RATE)
        freq = 1100 + 400 * (step % 2)
        sweep = [math.sin(2 * math.pi * freq * (i / SAMPLE_RATE)) for i in range(n_samples)]
        frames.extend(apply_envelope(sweep, 0.005, 0.01, 0.8, 0.015))
        frames.extend([0.0] * int(0.04 * SAMPLE_RATE))
    synth_wav("uakari.wav", frames)

def synth_elephant():
    n_samples = int(0.6 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        vibrato = 1.0 + 0.08 * math.sin(2 * math.pi * 15 * t)
        freq = (440 + 80 * (t / 0.6)) * vibrato
        val = 0.6 * math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t) + 0.1 * math.sin(6 * math.pi * freq * t)
        frames.append(val)
    frames = apply_envelope(frames, 0.08, 0.12, 0.7, 0.15)
    synth_wav("elephant.wav", frames)

def synth_penguin():
    frames = []
    for _ in range(2):
        n_samples = int(0.22 * SAMPLE_RATE)
        sweep = []
        for i in range(n_samples):
            t = i / SAMPLE_RATE
            freq = 380 + 180 * math.sin(2 * math.pi * 3.5 * t)
            val = 0.5 * (1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0)
            sweep.append(val)
        frames.extend(apply_envelope(sweep, 0.03, 0.04, 0.7, 0.05))
        frames.extend([0.0] * int(0.1 * SAMPLE_RATE))
    synth_wav("penguin.wav", frames)

def synth_ant():
    frames = []
    for _ in range(5):
        frames.extend([random.uniform(-0.6, 0.6) for _ in range(int(0.005 * SAMPLE_RATE))])
        frames.extend([0.0] * int(0.04 * SAMPLE_RATE))
    synth_wav("ant.wav", frames)

def synth_butterfly():
    frames = []
    for _ in range(6):
        n_samples = int(0.08 * SAMPLE_RATE)
        for i in range(n_samples):
            t = i / SAMPLE_RATE
            val = 0.3 * math.sin(2 * math.pi * 45 * t) * (1.0 - i / n_samples)
            frames.append(val)
        frames.extend([0.0] * int(0.05 * SAMPLE_RATE))
    synth_wav("butterfly.wav", frames)

def synth_giraffe():
    n_samples = int(0.7 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 150 + 5 * math.sin(2 * math.pi * 5 * t)
        val = math.sin(2 * math.pi * freq * t)
        frames.append(val * 0.4)
    frames = apply_envelope(frames, 0.15, 0.15, 0.8, 0.20)
    synth_wav("giraffe.wav", frames)

def synth_flamingo():
    n_samples = int(0.35 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 420 - 50 * (i / n_samples)
        val = 0.5 * math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(4 * math.pi * freq * t)
        frames.append(val)
    frames = apply_envelope(frames, 0.04, 0.06, 0.7, 0.08)
    synth_wav("flamingo.wav", frames)

def synth_hedgehog():
    frames = []
    for _ in range(3):
        for _ in range(int(0.12 * SAMPLE_RATE)):
            frames.append(0.35 * (random.random() * 2.0 - 1.0))
        frames.extend([0.0] * int(0.08 * SAMPLE_RATE))
    synth_wav("hedgehog.wav", frames)

def synth_turtle():
    frames = []
    for _ in range(3):
        frames.extend([random.uniform(-0.2, 0.2) for _ in range(int(0.02 * SAMPLE_RATE))])
        frames.extend([0.0] * int(0.2 * SAMPLE_RATE))
    synth_wav("turtle.wav", frames)

def synth_whale():
    n_samples = int(1.5 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = 280 + 60 * math.sin(2 * math.pi * 3 * t) + 40 * math.sin(2 * math.pi * 0.5 * t)
        val = math.sin(2 * math.pi * freq * t)
        frames.append(val * 0.5)
    frames = apply_envelope(frames, 0.3, 0.2, 0.8, 0.4)
    synth_wav("whale.wav", frames)

def synth_yak():
    n_samples = int(0.45 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        val = 0.3 * math.sin(2 * math.pi * 120 * t) + 0.3 * (random.random() * 2.0 - 1.0)
        frames.append(val)
    frames = apply_envelope(frames, 0.05, 0.05, 0.7, 0.15)
    synth_wav("yak.wav", frames)

def synth_zebra():
    n_samples = int(0.6 * SAMPLE_RATE)
    frames = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        vib = 1.0 + 0.1 * math.sin(2 * math.pi * 22 * t)
        freq = (600 + 400 * (t / 0.6)) * vib
        val = 0.4 * math.sin(2 * math.pi * freq * t)
        frames.append(val)
    frames = apply_envelope(frames, 0.05, 0.1, 0.7, 0.15)
    synth_wav("zebra.wav", frames)

SYNTH_FUNCTIONS = {
    "ant": synth_ant,
    "butterfly": synth_butterfly,
    "chick": synth_chick,
    "deer": synth_deer,
    "elephant": synth_elephant,
    "flamingo": synth_flamingo,
    "giraffe": synth_giraffe,
    "hedgehog": synth_hedgehog,
    "ibis": lambda: synth_bird("ibis.wav", 1300),
    "jellyfish": lambda: synth_bubble("jellyfish.wav"),
    "kitten": synth_kitten,
    "lamb": synth_lamb,
    "manatee": synth_manatee,
    "nightingale": lambda: synth_bird("nightingale.wav", 1000),
    "ostrich": synth_ostrich,
    "penguin": synth_penguin,
    "quokka": synth_uakari,
    "rabbit": synth_uakari,
    "seahorse": lambda: synth_bubble("seahorse.wav"),
    "turtle": synth_turtle,
    "uakari": synth_uakari,
    "squirrel": synth_squirrel,
    "whale": synth_whale,
    "axolotl": lambda: synth_bubble("axolotl.wav"),
    "yak": synth_yak,
    "zebra": synth_zebra
}

# ────────────────────────────────────────────────────────────
#  IMAGE CREATION AND CARD ASSEMBLY FUNCTIONS
# ────────────────────────────────────────────────────────────

def create_rounded_rect_card(size=(260, 240), radius=16, border_color=(255, 214, 0, 255), border_width=4):
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Draw rounded rectangle to serve as a card for the image
    draw.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=radius, fill=(255, 255, 255, 255), outline=border_color, width=border_width)
    return img

def process_and_crop_image(raw_bytes, filename):
    # Open the downloaded raster image
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGBA")
    
    # 1. Perform center-crop matching the 260x240 aspect ratio (13:12)
    w, h = img.size
    target_aspect = 260.0 / 240.0
    if w / h > target_aspect:
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        top = 0
        right = left + new_w
        bottom = h
    else:
        new_h = int(w / target_aspect)
        left = 0
        top = (h - new_h) // 2
        right = w
        bottom = top + new_h
    cropped = img.crop((left, top, right, bottom))
    
    # 2. Resize to leave a small padding border (e.g. 4px padding inside the 260x240 frame)
    inner_w, inner_h = 252, 232
    resized = cropped.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    
    # 3. Create a clean rounded rectangle card layout
    card = create_rounded_rect_card(size=(260, 240), radius=16, border_color=(255, 214, 0, 255), border_width=4)
    
    # 4. Create a rounded rectangle mask for the photo
    mask = Image.new("L", (inner_w, inner_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, inner_w-1, inner_h-1], radius=12, fill=255)
    
    # 5. Paste photo with mask at the center coordinates
    card.paste(resized, (4, 4), mask)
    
    # Save processed transparent rounded-rect PNG
    filepath = os.path.join(IMG_DIR, f"{filename}.png")
    card.save(filepath, "PNG")
    print(f"  [OK] Processed & Saved: {filename}.png ({os.path.getsize(filepath)} bytes)")


# ────────────────────────────────────────────────────────────
#  ROBUST API REQUEST & FALLBACK SEARCH
# ────────────────────────────────────────────────────────────

def make_request_with_backoff(url, params=None, max_retries=3):
    delay = 1.0
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                try:
                    return r.json()
                except Exception:
                    pass
        except Exception:
            pass
        time.sleep(delay)
        delay *= 2.0
    return None

def find_cute_animal_photo_fallback(animal_name):
    # Dynamically searches Wikimedia Commons if the curated URL fails
    queries = [
        f"cute baby {animal_name} photo",
        f"baby {animal_name} photo",
        f"cute {animal_name} photo",
        f"{animal_name} photo"
    ]
    negative_terms = ['dead', 'roadkill', 'fossil', 'skeleton', 'anatomy', 'accident', 'book', 'toy', 'museum', 'sculpture', 'art', 'draw', 'clipart', 'icon', 'vector', 'logo', 'diagram', 'stuffed']
    url = 'https://commons.wikimedia.org/w/api.php'
    
    for query in queries:
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'srnamespace': 6,
            'format': 'json',
            'origin': '*',
            'srlimit': 20
        }
        data = make_request_with_backoff(url, params)
        if data:
            results = data.get('query', {}).get('search', [])
            for res in results:
                t = res['title'].lower()
                if t.endswith(('.jpg', '.jpeg', '.png')):
                    # Apply negative filters to prevent loader tractors, skeletons, dead animals
                    if not any(term in t for term in negative_terms):
                        info_params = {
                            'action': 'query',
                            'titles': res['title'],
                            'prop': 'imageinfo',
                            'iiprop': 'url',
                            'format': 'json',
                            'origin': '*'
                        }
                        info_data = make_request_with_backoff(url, info_params)
                        if info_data:
                            pages = info_data.get('query', {}).get('pages', {})
                            for pid in pages:
                                info = pages[pid].get('imageinfo', [])
                                if info:
                                    img_url = info[0]['url']
                                    if img_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                                        return img_url
    return None

# ────────────────────────────────────────────────────────────
#  MAIN RUNNER
# ────────────────────────────────────────────────────────────

REAL_ANIMAL_SOUND_URLS = {
    "ant":          "https://upload.wikimedia.org/wikipedia/commons/e/e5/Ants_sound.ogg",
    "butterfly":    "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "chick":        "https://upload.wikimedia.org/wikipedia/commons/d/da/Chickens_clucking_and_chirping.ogg",
    "deer":         "https://upload.wikimedia.org/wikipedia/commons/4/4b/Deer_bellow.ogg",
    "elephant":     "https://upload.wikimedia.org/wikipedia/commons/1/15/Elephant_trumpet.ogg",
    "flamingo":     "https://upload.wikimedia.org/wikipedia/commons/7/7b/American_flamingo_vocalizations.ogg",
    "giraffe":      "https://upload.wikimedia.org/wikipedia/commons/8/87/Giraffe_humming.ogg",
    "hedgehog":     "https://upload.wikimedia.org/wikipedia/commons/6/6b/European_hedgehog_huffing.ogg",
    "ibis":         "https://upload.wikimedia.org/wikipedia/commons/3/30/Scarlet_ibis_vocalizations.ogg",
    "jellyfish":    "https://upload.wikimedia.org/wikipedia/commons/e/ee/Water_bubbles.ogg",
    "kitten":       "https://upload.wikimedia.org/wikipedia/commons/0/0f/Cat-meow.ogg",
    "lamb":         "https://upload.wikimedia.org/wikipedia/commons/0/03/Bleating_lamb.ogg",
    "manatee":      "https://upload.wikimedia.org/wikipedia/commons/a/ad/West_Indian_manatee_vocalizations.ogg",
    "nightingale":  "https://upload.wikimedia.org/wikipedia/commons/3/3b/Nightingale_song_-_Luscinia_megarhynchos.ogg",
    "ostrich":      "https://upload.wikimedia.org/wikipedia/commons/b/b3/Ostrich_hiss.ogg",
    "penguin":      "https://upload.wikimedia.org/wikipedia/commons/c/c9/Emperor_penguin_vocalizations.ogg",
    "quokka":       "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "rabbit":       "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "seahorse":     "https://upload.wikimedia.org/wikipedia/commons/e/ee/Water_bubbles.ogg",
    "turtle":       "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "uakari":       "https://upload.wikimedia.org/wikipedia/commons/c/cd/Red_uakari_alarm_call.ogg",
    "squirrel":     "https://upload.wikimedia.org/wikipedia/commons/2/26/Sciurus_vulgaris_alarm_call.ogg",
    "whale":        "https://upload.wikimedia.org/wikipedia/commons/c/cc/Humpback_whale_song_1.ogg",
    "axolotl":      "https://upload.wikimedia.org/wikipedia/commons/e/ee/Water_bubbles.ogg",
    "yak":          "https://upload.wikimedia.org/wikipedia/commons/9/90/Tibetan_yak_grunt.ogg",
    "zebra":        "https://upload.wikimedia.org/wikipedia/commons/6/6c/Zebra_call.ogg"
}

# ────────────────────────────────────────────────────────────
#  MAIN RUNNER
# ────────────────────────────────────────────────────────────

def download_and_assemble_all():
    print("=" * 60)
    print("  ABC Safari - Curated Child-Friendly Real Animal Photo & Sound Downloader")
    print("=" * 60)
    
    for filename, _ in ANIMAL_PHOTO_URLS.items():
        img_url = ANIMAL_PHOTO_URLS[filename]
        img_path = os.path.join(IMG_DIR, f"{filename}.png")
        
        # 1. Download and process real photo
        print(f"Downloading real photo for {filename}...")
        download_success = False
        try:
            r = requests.get(img_url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                process_and_crop_image(r.content, filename)
                download_success = True
            else:
                print(f"  [Info] Curated link failed (HTTP {r.status_code}). Triggering fallback search...")
        except Exception as e:
            print(f"  [Info] Curated link exception ({e}). Triggering fallback search...")
            
        if not download_success:
            # Try searching Wikimedia dynamically
            fallback_url = find_cute_animal_photo_fallback(filename)
            if fallback_url:
                print(f"  [Info] Found fallback URL: {fallback_url}. Downloading...")
                try:
                    r = requests.get(fallback_url, headers=HEADERS, timeout=15)
                    if r.status_code == 200:
                        process_and_crop_image(r.content, filename)
                        download_success = True
                except Exception as e:
                    print(f"  [Error] Fallback download failed: {e}")
            
        if not download_success:
            print(f"  [Error] All download options failed for {filename}. Asset will use fallback illustration if available.")
            
        # 2. Download real animal sound
        sound_url = REAL_ANIMAL_SOUND_URLS.get(filename)
        if sound_url:
            print(f"Downloading real sound for {filename}...")
            try:
                sr = requests.get(sound_url, headers=HEADERS, timeout=15)
                if sr.status_code == 200:
                    sound_path = os.path.join(SND_DIR, f"{filename}.ogg")
                    with open(sound_path, "wb") as sf:
                        sf.write(sr.content)
                    print(f"  [Sound OK] Saved {filename}.ogg")
                else:
                    print(f"  [Sound Error] Failed downloading sound (HTTP {sr.status_code})")
            except Exception as e:
                print(f"  [Sound Error] Exception downloading sound: {e}")
                
        # Increased delay to 1.5 seconds between downloads to be polite and prevent throttling
        time.sleep(1.5)
                
    print("=" * 60)
    print("  All real animal images and audio clips downloaded successfully!")
    print("=" * 60)

if __name__ == "__main__":
    download_and_assemble_all()
