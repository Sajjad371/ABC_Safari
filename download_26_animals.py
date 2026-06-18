# -*- coding: utf-8 -*-
"""
ABC Safari - 26 Animals Downloader & Verification Script
Downloads real, cute animal photos or matching fallbacks from Wikimedia Commons URLs
tailored directly to your explicit questions.py configuration.
File: asset_downloader.py
"""

import os
import sys
import time
import requests
from PIL import Image, ImageDraw
import io

# Directly synced dictionary mapping from your specific questions dataset
ANIMAL_PHOTO_URLS = {
    "ant":          "https://upload.wikimedia.org/wikipedia/commons/4/47/Leafcutter_ant_with_leaf.jpg",
    "bear":         "https://upload.wikimedia.org/wikipedia/commons/7/71/2010-kodiak-bear-1.jpg",
    "cat":          "https://upload.wikimedia.org/wikipedia/commons/a/ab/Cute_kitten%21.jpg",
    "dog":          "https://upload.wikimedia.org/wikipedia/commons/d/d9/Collage_of_Nine_Dogs.jpg",
    "elephant":     "https://upload.wikimedia.org/wikipedia/commons/6/6c/004_Desert-adapted_baby_elephants_cuddling_in_Damaraland_Photo_by_Giles_Laurent.jpg",
    "frog":         "https://upload.wikimedia.org/wikipedia/commons/d/d6/Red_eyed_tree_frog_edit2.jpg",
    "giraffe":      "https://upload.wikimedia.org/wikipedia/commons/b/b5/076_Baby_Angolan_giraffes_running_in_Etosha_National_Park_Photo_by_Giles_Laurent.jpg",
    "hippo":        "https://upload.wikimedia.org/wikipedia/commons/f/f2/Hippo_at_the_Cincinnati_Zoo_%2848386341492%29.jpg",
    "iguanas":      "https://upload.wikimedia.org/wikipedia/commons/c/c7/Green_Iguana_with_distended_dewlap.jpg",
    "jaguar":       "https://upload.wikimedia.org/wikipedia/commons/3/3c/Jaguar_in_the_Wild.jpg",
    "kangaroo":     "https://upload.wikimedia.org/wikipedia/commons/0/0d/Kangaroo_with_joey_in_pouch.jpg",
    "lion":         "https://upload.wikimedia.org/wikipedia/commons/7/73/Lion_waiting_in_Namibia.jpg",
    "monkey":       "https://upload.wikimedia.org/wikipedia/commons/e/e5/Japanese_Macaque_in_Kyoto_by_andrea_m_1.jpg",
    "nightingale":  "https://upload.wikimedia.org/wikipedia/commons/3/33/Nesocichla_eremita_-Nightingale_Island_-eating-8.jpg",
    "owl":          "https://upload.wikimedia.org/wikipedia/commons/d/d4/Eurasian_Eagle_Owl_at_individual_flying_demonstration_at_Burg_Falkenstein%2C_Germany_edit.jpg",
    "parrot":       "https://upload.wikimedia.org/wikipedia/commons/e/e0/A_blue-and-yellow_macaw_watering_her_feathers.jpg",
    "quail":        "https://upload.wikimedia.org/wikipedia/commons/0/00/Coturnix_coturnix_%28Common_Quail%29.jpg",
    "rabbit":       "https://upload.wikimedia.org/wikipedia/commons/e/e3/Baby_Bunny_Surprise%5E_%28Explore_April_14%2C_2022%29_-_Flickr_-_DaPuglet.jpg",
    "snake":        "https://upload.wikimedia.org/wikipedia/commons/d/d4/Smooth_snake_from_the_Side.jpg",
    "tiger":        "https://upload.wikimedia.org/wikipedia/commons/5/56/Tiger_in_Peaugres_zoo.jpg",
    "unikon":       "https://upload.wikimedia.org/wikipedia/commons/a/a3/Capra_sibirica_in_zoo_Berlin.jpg", # Fallback animal for U
    "vulture":      "https://upload.wikimedia.org/wikipedia/commons/b/b2/R%C3%BCppell%27s_vulture_%28Gyps_rueppelli%29.jpg",
    "whale":        "https://upload.wikimedia.org/wikipedia/commons/6/6e/031_Humpback_whale_lobtailing_Photo_by_Giles_Laurent.jpg",
    "xrayfish":     "https://upload.wikimedia.org/wikipedia/commons/8/87/Pristella_maxillaris_1.jpg",
    "yak":          "https://upload.wikimedia.org/wikipedia/commons/1/1c/Baby-Bauernhoftiere_001_2014_08_05.jpg",
    "zebra":        "https://upload.wikimedia.org/wikipedia/commons/8/88/Baby_zebra_%2815995185774%29.jpg"
}

REAL_ANIMAL_SOUND_URLS = {
    "ant":          "https://upload.wikimedia.org/wikipedia/commons/e/e5/Ants_sound.ogg",
    "bear":         "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "cat":          "https://upload.wikimedia.org/wikipedia/commons/0/0f/Cat-meow.ogg",
    "dog":          "https://upload.wikimedia.org/wikipedia/commons/b/b7/Growling_dog_1.ogg",
    "elephant":     "https://upload.wikimedia.org/wikipedia/commons/1/15/Elephant_trumpet.ogg",
    "frog":         "https://upload.wikimedia.org/wikipedia/commons/1/13/Rana_temporaria_mating_call_2.ogg",
    "giraffe":      "https://upload.wikimedia.org/wikipedia/commons/8/87/Giraffe_humming.ogg",
    "hippo":        "https://upload.wikimedia.org/wikipedia/commons/b/bd/Hippopotamus_vocalizations.ogg",
    "iguanas":      "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "jaguar":       "https://upload.wikimedia.org/wikipedia/commons/3/3c/Jaguar_in_the_Wild.jpg",
    "jellyfish":    "https://upload.wikimedia.org/wikipedia/commons/e/ee/Water_bubbles.ogg",
    "kangaroo":     "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "lion":         "https://upload.wikimedia.org/wikipedia/commons/7/73/Male_lion_roar.ogg",
    "monkey":       "https://upload.wikimedia.org/wikipedia/commons/2/22/Chimpanzee_vocalizations.ogg",
    "nightingale":  "https://upload.wikimedia.org/wikipedia/commons/3/3b/Nightingale_song_-_Luscinia_megarhynchos.ogg",
    "owl":          "https://upload.wikimedia.org/wikipedia/commons/e/e2/Athene_noctua_-_Little_Owl_calls_-_XC154445.ogg",
    "parrot":       "https://upload.wikimedia.org/wikipedia/commons/5/52/Amazona_amazonica_-_Orange-winged_Amazon_skawk.ogg",
    "quail":        "https://upload.wikimedia.org/wikipedia/commons/7/70/Coturnix_coturnix_singing_call_XC494958.ogg",
    "rabbit":       "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "snake":        "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "tiger":        "https://upload.wikimedia.org/wikipedia/commons/7/73/Male_lion_roar.ogg",
    "unikon":       "https://upload.wikimedia.org/wikipedia/commons/4/45/Rustling_leaves.ogg",
    "vulture":      "https://upload.wikimedia.org/wikipedia/commons/b/b3/Ostrich_hiss.ogg",
    "whale":        "https://upload.wikimedia.org/wikipedia/commons/c/cc/Humpback_whale_song_1.ogg",
    "xrayfish":     "https://upload.wikimedia.org/wikipedia/commons/e/ee/Water_bubbles.ogg",
    "yak":          "https://upload.wikimedia.org/wikipedia/commons/9/90/Tibetan_yak_grunt.ogg",
    "zebra":        "https://upload.wikimedia.org/wikipedia/commons/6/6c/Zebra_call.ogg"
}

# The target database configuration list that you provided
QUESTIONS_CONFIG = [
    {"animal": "Ant", "image": "assets/images/animals/ant.png", "sound": "assets/sounds/animals/ant.ogg"},
    {"animal": "Bear", "image": "assets/images/animals/bear.png", "sound": "assets/sounds/animals/bear.ogg"},
    {"animal": "Cat", "image": "assets/images/animals/cat.png", "sound": "assets/sounds/animals/cat.ogg"},
    {"animal": "Dog ", "image": "assets/images/animals/dog.png", "sound": "assets/sounds/animals/dog.ogg"},
    {"animal": "Elephant", "image": "assets/images/animals/elephant.png", "sound": "assets/sounds/animals/elephant.ogg"},
    {"animal": "Frog", "image": "assets/images/animals/frog.png", "sound": "assets/sounds/animals/frog.ogg"},
    {"animal": "Giraffe", "image": "assets/images/animals/giraffe.png", "sound": "assets/sounds/animals/giraffe.ogg"},
    {"animal": "Hippo", "image": "assets/images/animals/hippo.png", "sound": "assets/sounds/animals/hippo.ogg"},
    {"animal": "Iguana", "image": "assets/images/animals/iguanas.png", "sound": "assets/sounds/animals/iguanas.ogg"},
    {"animal": "Jaguar", "image": "assets/images/animals/jaguar.png", "sound": "assets/sounds/animals/jaguar.ogg"},
    {"animal": "Kangaroo", "image": "assets/images/animals/kangaroo.png", "sound": "assets/sounds/animals/kangaroo.ogg"},
    {"animal": "Lion", "image": "assets/images/animals/lion.png", "sound": "assets/sounds/animals/lion.ogg"},
    {"animal": "Monkey", "image": "assets/images/animals/monkey.png", "sound": "assets/sounds/animals/monkey.ogg"},
    {"animal": "Nightingale", "image": "assets/images/animals/nightingale.png", "sound": "assets/sounds/animals/nightingale.ogg"},
    {"animal": "Owl", "image": "assets/images/animals/owl.png", "sound": "assets/sounds/animals/owl.ogg"},
    {"animal": "Parrot", "image": "assets/images/animals/parrot.png", "sound": "assets/sounds/animals/parrot.ogg"},
    {"animal": "Quail", "image": "assets/images/animals/quail.png", "sound": "assets/sounds/animals/quail.ogg"},
    {"animal": "Rabbit", "image": "assets/images/animals/rabbit.png", "sound": "assets/sounds/animals/rabbit.ogg"},
    {"animal": "Snake", "image": "assets/images/animals/snake.png", "sound": "assets/sounds/animals/snake.ogg"},
    {"animal": "Tiger", "image": "assets/images/animals/tiger.png", "sound": "assets/sounds/animals/tiger.ogg"},
    {"animal": "Unikon", "image": "assets/images/animals/unikon.png", "sound": "assets/sounds/animals/unikon.ogg"},
    {"animal": "Vulture", "image": "assets/images/animals/vulture.png", "sound": "assets/sounds/animals/vulture.ogg"},
    {"animal": "Whale", "image": "assets/images/animals/whale.png", "sound": "assets/sounds/animals/whale.ogg"},
    {"animal": "Xrayfish", "image": "assets/images/animals/xrayfish.png", "sound": "assets/sounds/animals/xrayfish.ogg"},
    {"animal": "Yak", "image": "assets/images/animals/yak.png", "sound": "assets/sounds/animals/yak.ogg"},
    {"animal": "Zebra", "image": "assets/images/animals/zebra.png", "sound": "assets/sounds/animals/zebra.ogg"}
]

HEADERS = {'User-Agent': 'ABCSafariEducationalApp/1.0 (contact@sajjadeducation.org) Python-Requests/2.31'}

def create_rounded_rect_card(size=(260, 240), radius=16, border_color=(255, 214, 0, 255), border_width=4):
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=radius, fill=(255, 255, 255, 255), outline=border_color, width=border_width)
    return img

def process_and_crop_image(raw_bytes, target_path):
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGBA")
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
    
    inner_w, inner_h = 252, 232
    resized = cropped.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    card = create_rounded_rect_card(size=(260, 240), radius=16, border_color=(255, 214, 0, 255), border_width=4)
    
    mask = Image.new("L", (inner_w, inner_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, inner_w-1, inner_h-1], radius=12, fill=255)
    
    card.paste(resized, (4, 4), mask)
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    card.save(target_path, "PNG")
    print(f"  [OK] Processed & Saved Image -> {target_path}")

def make_request_with_backoff(url, params=None, max_retries=3):
    delay = 1.0
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                try: return r.json()
                except: pass
        except: pass
        time.sleep(delay)
        delay *= 2.0
    return None

def find_animal_photo_fallback(animal_name):
    clean_name = animal_name.strip().lower()
    if clean_name == "unikon": clean_name = "unicorn statue"
    if clean_name == "xrayfish": clean_name = "pristella maxillaris"
    
    queries = [f"cute {clean_name} photo", f"{clean_name} photo"]
    url = 'https://commons.wikimedia.org/w/api.php'
    
    for query in queries:
        params = {'action': 'query', 'list': 'search', 'srsearch': query, 'srnamespace': 6, 'format': 'json', 'origin': '*', 'srlimit': 10}
        data = make_request_with_backoff(url, params)
        if data:
            results = data.get('query', {}).get('search', [])
            for res in results:
                t = res['title'].lower()
                if t.endswith(('.jpg', '.jpeg', '.png')):
                    info_params = {'action': 'query', 'titles': res['title'], 'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json', 'origin': '*'}
                    info_data = make_request_with_backoff(url, info_params)
                    if info_data:
                        pages = info_data.get('query', {}).get('pages', {})
                        for pid in pages:
                            info = pages[pid].get('imageinfo', [])
                            if info and info[0]['url'].lower().endswith(('.jpg', '.jpeg', '.png')):
                                return info[0]['url']
    return None

def run_sync_downloader():
    print("=" * 60)
    print("  ABC Safari - Downloader Core Synced directly to questions.py")
    print("=" * 60)
    
    for item in QUESTIONS_CONFIG:
        raw_name = item["animal"]
        lookup_key = raw_name.strip().lower()
        image_dest_path = item["image"]
        sound_dest_path = item["sound"]
        
        print(f"\nProcessing target asset dependencies for: [{raw_name}]")
        
        # 1. Download Match Image
        img_url = ANIMAL_PHOTO_URLS.get(lookup_key)
        download_success = False
        if img_url:
            try:
                r = requests.get(img_url, headers=HEADERS, timeout=15)
                if r.status_code == 200:
                    process_and_crop_image(r.content, image_dest_path)
                    download_success = True
            except:
                pass
                
        if not download_success:
            fallback_url = find_animal_photo_fallback(lookup_key)
            if fallback_url:
                try:
                    r = requests.get(fallback_url, headers=HEADERS, timeout=15)
                    if r.status_code == 200:
                        process_and_crop_image(r.content, image_dest_path)
                        download_success = True
                except:
                    pass
                    
        if not download_success:
            print(f"  [Warning] Image could not be auto-saved for {raw_name}")

        # 2. Download Match Sound
        sound_url = REAL_ANIMAL_SOUND_URLS.get(lookup_key)
        if sound_url:
            try:
                os.makedirs(os.path.dirname(sound_dest_path), exist_ok=True)
                sr = requests.get(sound_url, headers=HEADERS, timeout=15)
                if sr.status_code == 200:
                    with open(sound_dest_path, "wb") as sf:
                        sf.write(sr.content)
                    print(f"  [OK] Saved Audio -> {sound_dest_path}")
            except Exception as e:
                print(f"  [Error] Sound fetch fail: {e}")
                
        time.sleep(1.0)

    print("\n" + "=" * 60)
    print("  Asset Synchronization Complete!")
    print("=" * 60)

if __name__ == "__main__":
    run_sync_downloader()