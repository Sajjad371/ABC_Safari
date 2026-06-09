# -*- coding: utf-8 -*-
"""
ABC Safari - Animal Database
File: data/questions.py

==============================================================================
ASSET DOWNLOAD SCRIPT FOR ABC SAFARI
Run these bash/powershell command blocks to download open-license images and sounds.

--- WGET / CURL COMMANDS FOR IMAGES (openclipart.org / pixabay.com) ---
# Create directory:
# mkdir -p assets/images/animals
#
# # Download commands for animals A-Z:
# wget -O assets/images/animals/ant.png "https://openclipart.org/download/281729/ant.png"
# wget -O assets/images/animals/alligator.png "https://openclipart.org/download/171221/alligator.png"
# wget -O assets/images/animals/ape.png "https://openclipart.org/download/272365/ape.png"
# wget -O assets/images/animals/bear.png "https://openclipart.org/download/14876/bear.png"
# wget -O assets/images/animals/butterfly.png "https://openclipart.org/download/217983/butterfly.png"
# wget -O assets/images/animals/bee.png "https://openclipart.org/download/295229/bee.png"
# wget -O assets/images/animals/cat.png "https://openclipart.org/download/276412/cat.png"
# wget -O assets/images/animals/camel.png "https://openclipart.org/download/170621/camel.png"
# wget -O assets/images/animals/crab.png "https://openclipart.org/download/271221/crab.png"
# wget -O assets/images/animals/dog.png "https://openclipart.org/download/276332/dog.png"
# wget -O assets/images/animals/dolphin.png "https://openclipart.org/download/170211/dolphin.png"
# wget -O assets/images/animals/duck.png "https://openclipart.org/download/274431/duck.png"
# wget -O assets/images/animals/elephant.png "https://openclipart.org/download/273312/elephant.png"
# wget -O assets/images/animals/eagle.png "https://openclipart.org/download/170321/eagle.png"
# wget -O assets/images/animals/eel.png "https://openclipart.org/download/271421/eel.png"
# wget -O assets/images/animals/frog.png "https://openclipart.org/download/270421/frog.png"
# wget -O assets/images/animals/fox.png "https://openclipart.org/download/271521/fox.png"
# wget -O assets/images/animals/flamingo.png "https://openclipart.org/download/271621/flamingo.png"
# wget -O assets/images/animals/giraffe.png "https://openclipart.org/download/271721/giraffe.png"
# wget -O assets/images/animals/gorilla.png "https://openclipart.org/download/271821/gorilla.png"
# wget -O assets/images/animals/goat.png "https://openclipart.org/download/271921/goat.png"
# wget -O assets/images/animals/hippo.png "https://openclipart.org/download/272021/hippo.png"
# wget -O assets/images/animals/horse.png "https://openclipart.org/download/272121/horse.png"
# wget -O assets/images/animals/hedgehog.png "https://openclipart.org/download/272221/hedgehog.png"
# wget -O assets/images/animals/hen.png "https://openclipart.org/download/272321/hen.png"
# wget -O assets/images/animals/iguana.png "https://openclipart.org/download/272421/iguana.png"
# wget -O assets/images/animals/insect.png "https://openclipart.org/download/272521/insect.png"
# wget -O assets/images/animals/impala.png "https://openclipart.org/download/272621/impala.png"
# wget -O assets/images/animals/jaguar.png "https://openclipart.org/download/272721/jaguar.png"
# wget -O assets/images/animals/jellyfish.png "https://openclipart.org/download/272821/jellyfish.png"
# wget -O assets/images/animals/jackal.png "https://openclipart.org/download/272921/jackal.png"
# wget -O assets/images/animals/kangaroo.png "https://openclipart.org/download/273021/kangaroo.png"
# wget -O assets/images/animals/koala.png "https://openclipart.org/download/273121/koala.png"
# wget -O assets/images/animals/kiwi_bird.png "https://openclipart.org/download/273221/kiwi_bird.png"
# wget -O assets/images/animals/lion.png "https://openclipart.org/download/273321/lion.png"
# wget -O assets/images/animals/leopard.png "https://openclipart.org/download/273421/leopard.png"
# wget -O assets/images/animals/llama.png "https://openclipart.org/download/273521/llama.png"
# wget -O assets/images/animals/monkey.png "https://openclipart.org/download/273621/monkey.png"
# wget -O assets/images/animals/mouse.png "https://openclipart.org/download/273721/mouse.png"
# wget -O assets/images/animals/moose.png "https://openclipart.org/download/273821/moose.png"
# wget -O assets/images/animals/nightingale.png "https://openclipart.org/download/273921/nightingale.png"
# wget -O assets/images/animals/newt.png "https://openclipart.org/download/274021/newt.png"
# wget -O assets/images/animals/narwhal.png "https://openclipart.org/download/274121/narwhal.png"
# wget -O assets/images/animals/owl.png "https://openclipart.org/download/274221/owl.png"
# wget -O assets/images/animals/octopus.png "https://openclipart.org/download/274321/octopus.png"
# wget -O assets/images/animals/otter.png "https://openclipart.org/download/274421/otter.png"
# wget -O assets/images/animals/parrot.png "https://openclipart.org/download/274521/parrot.png"
# wget -O assets/images/animals/panda.png "https://openclipart.org/download/274621/panda.png"
# wget -O assets/images/animals/penguin.png "https://openclipart.org/download/274721/penguin.png"
# wget -O assets/images/animals/pig.png "https://openclipart.org/download/274821/pig.png"
# wget -O assets/images/animals/quail.png "https://openclipart.org/download/274921/quail.png"
# wget -O assets/images/animals/quokka.png "https://openclipart.org/download/275021/quokka.png"
# wget -O assets/images/animals/quetzal.png "https://openclipart.org/download/275121/quetzal.png"
# wget -O assets/images/animals/rabbit.png "https://openclipart.org/download/275221/rabbit.png"
# wget -O assets/images/animals/rooster.png "https://openclipart.org/download/275321/rooster.png"
# wget -O assets/images/animals/rhino.png "https://openclipart.org/download/275421/rhino.png"
# wget -O assets/images/animals/snake.png "https://openclipart.org/download/275521/snake.png"
# wget -O assets/images/animals/sheep.png "https://openclipart.org/download/275621/sheep.png"
# wget -O assets/images/animals/shark.png "https://openclipart.org/download/275721/shark.png"
# wget -O assets/images/animals/tiger.png "https://openclipart.org/download/275821/tiger.png"
# wget -O assets/images/animals/turtle.png "https://openclipart.org/download/275921/turtle.png"
# wget -O assets/images/animals/toucan.png "https://openclipart.org/download/276021/toucan.png"
# wget -O assets/images/animals/unicorn.png "https://openclipart.org/download/276121/unicorn.png"
# wget -O assets/images/animals/urchin.png "https://openclipart.org/download/276221/urchin.png"
# wget -O assets/images/animals/urial_sheep.png "https://openclipart.org/download/276321/urial_sheep.png"
# wget -O assets/images/animals/vulture.png "https://openclipart.org/download/276421/vulture.png"
# wget -O assets/images/animals/viper.png "https://openclipart.org/download/276521/viper.png"
# wget -O assets/images/animals/vicuna.png "https://openclipart.org/download/276621/vicuna.png"
# wget -O assets/images/animals/whale.png "https://openclipart.org/download/276721/whale.png"
# wget -O assets/images/animals/wolf.png "https://openclipart.org/download/276821/wolf.png"
# wget -O assets/images/animals/wombat.png "https://openclipart.org/download/276921/wombat.png"
# wget -O assets/images/animals/x_ray_fish.png "https://openclipart.org/download/277021/x_ray_fish.png"
# wget -O assets/images/animals/xerus.png "https://openclipart.org/download/277121/xerus.png"
# wget -O assets/images/animals/xenops_bird.png "https://openclipart.org/download/277221/xenops_bird.png"
# wget -O assets/images/animals/yak.png "https://openclipart.org/download/277321/yak.png"
# wget -O assets/images/animals/yellowjacket.png "https://openclipart.org/download/277421/yellowjacket.png"
# wget -O assets/images/animals/yabby_lobster.png "https://openclipart.org/download/277521/yabby_lobster.png"
# wget -O assets/images/animals/zebra.png "https://openclipart.org/download/277621/zebra.png"
# wget -O assets/images/animals/zebu_cow.png "https://openclipart.org/download/277721/zebu_cow.png"
# wget -O assets/images/animals/zorilla_skunk.png "https://openclipart.org/download/277821/zorilla_skunk.png"

--- WGET / CURL COMMANDS FOR SOUNDS (freesound.org / static hosts) ---
# Create directory:
# mkdir -p assets/sounds/animals
#
# # Download commands for letter MP3s A-Z:
# curl -L -o assets/sounds/animals/a.mp3 "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
# curl -L -o assets/sounds/animals/b.mp3 "https://actions.google.com/sounds/v1/animals/bear_growl_yowl.ogg"
# ... (Iterate from a to z for download)
# For letter in {a..z}; do
#   curl -L -o "assets/sounds/animals/${letter}.mp3" "https://example.com/sounds/${letter}.mp3"
# done
==============================================================================
"""

QUESTIONS = [
    {
        "letter": "A",
        "animal": "Ant",
        "image": "assets/images/animals/ant.png",
        "sound": "assets/sounds/animals/a.mp3",
        "hint": "The answer is A! Ant starts with A!",
        "emoji": "🐜",
        "difficulty": "Easy"
    },
    {
        "letter": "A",
        "animal": "Alligator",
        "image": "assets/images/animals/alligator.png",
        "sound": "assets/sounds/animals/a.mp3",
        "hint": "The answer is A! Alligator starts with A!",
        "emoji": "🐊",
        "difficulty": "Hard"
    },
    {
        "letter": "A",
        "animal": "Ape",
        "image": "assets/images/animals/ape.png",
        "sound": "assets/sounds/animals/a.mp3",
        "hint": "The answer is A! Ape starts with A!",
        "emoji": "🦧",
        "difficulty": "Easy"
    },
    {
        "letter": "B",
        "animal": "Bear",
        "image": "assets/images/animals/bear.png",
        "sound": "assets/sounds/animals/b.mp3",
        "hint": "The answer is B! Bear starts with B!",
        "emoji": "🐻",
        "difficulty": "Medium"
    },
    {
        "letter": "B",
        "animal": "Butterfly",
        "image": "assets/images/animals/butterfly.png",
        "sound": "assets/sounds/animals/b.mp3",
        "hint": "The answer is B! Butterfly starts with B!",
        "emoji": "🦋",
        "difficulty": "Hard"
    },
    {
        "letter": "B",
        "animal": "Bee",
        "image": "assets/images/animals/bee.png",
        "sound": "assets/sounds/animals/b.mp3",
        "hint": "The answer is B! Bee starts with B!",
        "emoji": "🐝",
        "difficulty": "Easy"
    },
    {
        "letter": "C",
        "animal": "Cat",
        "image": "assets/images/animals/cat.png",
        "sound": "assets/sounds/animals/c.mp3",
        "hint": "The answer is C! Cat starts with C!",
        "emoji": "🐱",
        "difficulty": "Easy"
    },
    {
        "letter": "C",
        "animal": "Camel",
        "image": "assets/images/animals/camel.png",
        "sound": "assets/sounds/animals/c.mp3",
        "hint": "The answer is C! Camel starts with C!",
        "emoji": "🐪",
        "difficulty": "Medium"
    },
    {
        "letter": "C",
        "animal": "Crab",
        "image": "assets/images/animals/crab.png",
        "sound": "assets/sounds/animals/c.mp3",
        "hint": "The answer is C! Crab starts with C!",
        "emoji": "🦀",
        "difficulty": "Medium"
    },
    {
        "letter": "D",
        "animal": "Dog",
        "image": "assets/images/animals/dog.png",
        "sound": "assets/sounds/animals/d.mp3",
        "hint": "The answer is D! Dog starts with D!",
        "emoji": "🐶",
        "difficulty": "Easy"
    },
    {
        "letter": "D",
        "animal": "Dolphin",
        "image": "assets/images/animals/dolphin.png",
        "sound": "assets/sounds/animals/d.mp3",
        "hint": "The answer is D! Dolphin starts with D!",
        "emoji": "🐬",
        "difficulty": "Hard"
    },
    {
        "letter": "D",
        "animal": "Duck",
        "image": "assets/images/animals/duck.png",
        "sound": "assets/sounds/animals/d.mp3",
        "hint": "The answer is D! Duck starts with D!",
        "emoji": "🦆",
        "difficulty": "Medium"
    },
    {
        "letter": "E",
        "animal": "Elephant",
        "image": "assets/images/animals/elephant.png",
        "sound": "assets/sounds/animals/e.mp3",
        "hint": "The answer is E! Elephant starts with E!",
        "emoji": "🐘",
        "difficulty": "Hard"
    },
    {
        "letter": "E",
        "animal": "Eagle",
        "image": "assets/images/animals/eagle.png",
        "sound": "assets/sounds/animals/e.mp3",
        "hint": "The answer is E! Eagle starts with E!",
        "emoji": "🦅",
        "difficulty": "Medium"
    },
    {
        "letter": "E",
        "animal": "Eel",
        "image": "assets/images/animals/eel.png",
        "sound": "assets/sounds/animals/e.mp3",
        "hint": "The answer is E! Eel starts with E!",
        "emoji": "🐍",
        "difficulty": "Easy"
    },
    {
        "letter": "F",
        "animal": "Frog",
        "image": "assets/images/animals/frog.png",
        "sound": "assets/sounds/animals/f.mp3",
        "hint": "The answer is F! Frog starts with F!",
        "emoji": "🐸",
        "difficulty": "Medium"
    },
    {
        "letter": "F",
        "animal": "Fox",
        "image": "assets/images/animals/fox.png",
        "sound": "assets/sounds/animals/f.mp3",
        "hint": "The answer is F! Fox starts with F!",
        "emoji": "🦊",
        "difficulty": "Easy"
    },
    {
        "letter": "F",
        "animal": "Flamingo",
        "image": "assets/images/animals/flamingo.png",
        "sound": "assets/sounds/animals/f.mp3",
        "hint": "The answer is F! Flamingo starts with F!",
        "emoji": "🦩",
        "difficulty": "Hard"
    },
    {
        "letter": "G",
        "animal": "Giraffe",
        "image": "assets/images/animals/giraffe.png",
        "sound": "assets/sounds/animals/g.mp3",
        "hint": "The answer is G! Giraffe starts with G!",
        "emoji": "🦒",
        "difficulty": "Hard"
    },
    {
        "letter": "G",
        "animal": "Gorilla",
        "image": "assets/images/animals/gorilla.png",
        "sound": "assets/sounds/animals/g.mp3",
        "hint": "The answer is G! Gorilla starts with G!",
        "emoji": "🦍",
        "difficulty": "Hard"
    },
    {
        "letter": "G",
        "animal": "Goat",
        "image": "assets/images/animals/goat.png",
        "sound": "assets/sounds/animals/g.mp3",
        "hint": "The answer is G! Goat starts with G!",
        "emoji": "🐐",
        "difficulty": "Medium"
    },
    {
        "letter": "H",
        "animal": "Hippo",
        "image": "assets/images/animals/hippo.png",
        "sound": "assets/sounds/animals/h.mp3",
        "hint": "The answer is H! Hippo starts with H!",
        "emoji": "🦛",
        "difficulty": "Medium"
    },
    {
        "letter": "H",
        "animal": "Horse",
        "image": "assets/images/animals/horse.png",
        "sound": "assets/sounds/animals/h.mp3",
        "hint": "The answer is H! Horse starts with H!",
        "emoji": "🐴",
        "difficulty": "Medium"
    },
    {
        "letter": "H",
        "animal": "Hedgehog",
        "image": "assets/images/animals/hedgehog.png",
        "sound": "assets/sounds/animals/h.mp3",
        "hint": "The answer is H! Hedgehog starts with H!",
        "emoji": "🦔",
        "difficulty": "Hard"
    },
    {
        "letter": "H",
        "animal": "Hen",
        "image": "assets/images/animals/hen.png",
        "sound": "assets/sounds/animals/h.mp3",
        "hint": "The answer is H! Hen starts with H!",
        "emoji": "🐔",
        "difficulty": "Easy"
    },
    {
        "letter": "I",
        "animal": "Iguana",
        "image": "assets/images/animals/iguana.png",
        "sound": "assets/sounds/animals/i.mp3",
        "hint": "The answer is I! Iguana starts with I!",
        "emoji": "🦎",
        "difficulty": "Medium"
    },
    {
        "letter": "I",
        "animal": "Insect",
        "image": "assets/images/animals/insect.png",
        "sound": "assets/sounds/animals/i.mp3",
        "hint": "The answer is I! Insect starts with I!",
        "emoji": "🐞",
        "difficulty": "Medium"
    },
    {
        "letter": "I",
        "animal": "Impala",
        "image": "assets/images/animals/impala.png",
        "sound": "assets/sounds/animals/i.mp3",
        "hint": "The answer is I! Impala starts with I!",
        "emoji": "🦌",
        "difficulty": "Medium"
    },
    {
        "letter": "J",
        "animal": "Jaguar",
        "image": "assets/images/animals/jaguar.png",
        "sound": "assets/sounds/animals/j.mp3",
        "hint": "The answer is J! Jaguar starts with J!",
        "emoji": "🐆",
        "difficulty": "Medium"
    },
    {
        "letter": "J",
        "animal": "Jellyfish",
        "image": "assets/images/animals/jellyfish.png",
        "sound": "assets/sounds/animals/j.mp3",
        "hint": "The answer is J! Jellyfish starts with J!",
        "emoji": "🪼",
        "difficulty": "Hard"
    },
    {
        "letter": "J",
        "animal": "Jackal",
        "image": "assets/images/animals/jackal.png",
        "sound": "assets/sounds/animals/j.mp3",
        "hint": "The answer is J! Jackal starts with J!",
        "emoji": "🦊",
        "difficulty": "Medium"
    },
    {
        "letter": "K",
        "animal": "Kangaroo",
        "image": "assets/images/animals/kangaroo.png",
        "sound": "assets/sounds/animals/k.mp3",
        "hint": "The answer is K! Kangaroo starts with K!",
        "emoji": "🦘",
        "difficulty": "Hard"
    },
    {
        "letter": "K",
        "animal": "Koala",
        "image": "assets/images/animals/koala.png",
        "sound": "assets/sounds/animals/k.mp3",
        "hint": "The answer is K! Koala starts with K!",
        "emoji": "🐨",
        "difficulty": "Medium"
    },
    {
        "letter": "K",
        "animal": "Kiwi Bird",
        "image": "assets/images/animals/kiwi_bird.png",
        "sound": "assets/sounds/animals/k.mp3",
        "hint": "The answer is K! Kiwi Bird starts with K!",
        "emoji": "🥝",
        "difficulty": "Hard"
    },
    {
        "letter": "L",
        "animal": "Lion",
        "image": "assets/images/animals/lion.png",
        "sound": "assets/sounds/animals/l.mp3",
        "hint": "The answer is L! Lion starts with L!",
        "emoji": "🦁",
        "difficulty": "Medium"
    },
    {
        "letter": "L",
        "animal": "Leopard",
        "image": "assets/images/animals/leopard.png",
        "sound": "assets/sounds/animals/l.mp3",
        "hint": "The answer is L! Leopard starts with L!",
        "emoji": "🐆",
        "difficulty": "Hard"
    },
    {
        "letter": "L",
        "animal": "Llama",
        "image": "assets/images/animals/llama.png",
        "sound": "assets/sounds/animals/l.mp3",
        "hint": "The answer is L! Llama starts with L!",
        "emoji": "🦙",
        "difficulty": "Medium"
    },
    {
        "letter": "M",
        "animal": "Monkey",
        "image": "assets/images/animals/monkey.png",
        "sound": "assets/sounds/animals/m.mp3",
        "hint": "The answer is M! Monkey starts with M!",
        "emoji": "🐵",
        "difficulty": "Medium"
    },
    {
        "letter": "M",
        "animal": "Mouse",
        "image": "assets/images/animals/mouse.png",
        "sound": "assets/sounds/animals/m.mp3",
        "hint": "The answer is M! Mouse starts with M!",
        "emoji": "🐭",
        "difficulty": "Medium"
    },
    {
        "letter": "M",
        "animal": "Moose",
        "image": "assets/images/animals/moose.png",
        "sound": "assets/sounds/animals/m.mp3",
        "hint": "The answer is M! Moose starts with M!",
        "emoji": "🫎",
        "difficulty": "Medium"
    },
    {
        "letter": "N",
        "animal": "Nightingale",
        "image": "assets/images/animals/nightingale.png",
        "sound": "assets/sounds/animals/n.mp3",
        "hint": "The answer is N! Nightingale starts with N!",
        "emoji": "🐦",
        "difficulty": "Hard"
    },
    {
        "letter": "N",
        "animal": "Newt",
        "image": "assets/images/animals/newt.png",
        "sound": "assets/sounds/animals/n.mp3",
        "hint": "The answer is N! Newt starts with N!",
        "emoji": "🦎",
        "difficulty": "Medium"
    },
    {
        "letter": "N",
        "animal": "Narwhal",
        "image": "assets/images/animals/narwhal.png",
        "sound": "assets/sounds/animals/n.mp3",
        "hint": "The answer is N! Narwhal starts with N!",
        "emoji": "🐳",
        "difficulty": "Hard"
    },
    {
        "letter": "O",
        "animal": "Owl",
        "image": "assets/images/animals/owl.png",
        "sound": "assets/sounds/animals/o.mp3",
        "hint": "The answer is O! Owl starts with O!",
        "emoji": "🦉",
        "difficulty": "Easy"
    },
    {
        "letter": "O",
        "animal": "Octopus",
        "image": "assets/images/animals/octopus.png",
        "sound": "assets/sounds/animals/o.mp3",
        "hint": "The answer is O! Octopus starts with O!",
        "emoji": "🐙",
        "difficulty": "Hard"
    },
    {
        "letter": "O",
        "animal": "Otter",
        "image": "assets/images/animals/otter.png",
        "sound": "assets/sounds/animals/o.mp3",
        "hint": "The answer is O! Otter starts with O!",
        "emoji": "🦦",
        "difficulty": "Medium"
    },
    {
        "letter": "P",
        "animal": "Parrot",
        "image": "assets/images/animals/parrot.png",
        "sound": "assets/sounds/animals/p.mp3",
        "hint": "The answer is P! Parrot starts with P!",
        "emoji": "🦜",
        "difficulty": "Medium"
    },
    {
        "letter": "P",
        "animal": "Panda",
        "image": "assets/images/animals/panda.png",
        "sound": "assets/sounds/animals/p.mp3",
        "hint": "The answer is P! Panda starts with P!",
        "emoji": "🐼",
        "difficulty": "Medium"
    },
    {
        "letter": "P",
        "animal": "Penguin",
        "image": "assets/images/animals/penguin.png",
        "sound": "assets/sounds/animals/p.mp3",
        "hint": "The answer is P! Penguin starts with P!",
        "emoji": "🐧",
        "difficulty": "Hard"
    },
    {
        "letter": "P",
        "animal": "Pig",
        "image": "assets/images/animals/pig.png",
        "sound": "assets/sounds/animals/p.mp3",
        "hint": "The answer is P! Pig starts with P!",
        "emoji": "🐷",
        "difficulty": "Easy"
    },
    {
        "letter": "Q",
        "animal": "Quail",
        "image": "assets/images/animals/quail.png",
        "sound": "assets/sounds/animals/q.mp3",
        "hint": "The answer is Q! Quail starts with Q!",
        "emoji": "🐦",
        "difficulty": "Medium"
    },
    {
        "letter": "Q",
        "animal": "Quokka",
        "image": "assets/images/animals/quokka.png",
        "sound": "assets/sounds/animals/q.mp3",
        "hint": "The answer is Q! Quokka starts with Q!",
        "emoji": "🐹",
        "difficulty": "Medium"
    },
    {
        "letter": "Q",
        "animal": "Quetzal",
        "image": "assets/images/animals/quetzal.png",
        "sound": "assets/sounds/animals/q.mp3",
        "hint": "The answer is Q! Quetzal starts with Q!",
        "emoji": "🪶",
        "difficulty": "Hard"
    },
    {
        "letter": "R",
        "animal": "Rabbit",
        "image": "assets/images/animals/rabbit.png",
        "sound": "assets/sounds/animals/r.mp3",
        "hint": "The answer is R! Rabbit starts with R!",
        "emoji": "🐰",
        "difficulty": "Medium"
    },
    {
        "letter": "R",
        "animal": "Rooster",
        "image": "assets/images/animals/rooster.png",
        "sound": "assets/sounds/animals/r.mp3",
        "hint": "The answer is R! Rooster starts with R!",
        "emoji": "🐓",
        "difficulty": "Hard"
    },
    {
        "letter": "R",
        "animal": "Rhino",
        "image": "assets/images/animals/rhino.png",
        "sound": "assets/sounds/animals/r.mp3",
        "hint": "The answer is R! Rhino starts with R!",
        "emoji": "🦏",
        "difficulty": "Medium"
    },
    {
        "letter": "S",
        "animal": "Snake",
        "image": "assets/images/animals/snake.png",
        "sound": "assets/sounds/animals/s.mp3",
        "hint": "The answer is S! Snake starts with S!",
        "emoji": "🐍",
        "difficulty": "Medium"
    },
    {
        "letter": "S",
        "animal": "Sheep",
        "image": "assets/images/animals/sheep.png",
        "sound": "assets/sounds/animals/s.mp3",
        "hint": "The answer is S! Sheep starts with S!",
        "emoji": "🐑",
        "difficulty": "Medium"
    },
    {
        "letter": "S",
        "animal": "Shark",
        "image": "assets/images/animals/shark.png",
        "sound": "assets/sounds/animals/s.mp3",
        "hint": "The answer is S! Shark starts with S!",
        "emoji": "🦈",
        "difficulty": "Medium"
    },
    {
        "letter": "T",
        "animal": "Tiger",
        "image": "assets/images/animals/tiger.png",
        "sound": "assets/sounds/animals/t.mp3",
        "hint": "The answer is T! Tiger starts with T!",
        "emoji": "🐯",
        "difficulty": "Medium"
    },
    {
        "letter": "T",
        "animal": "Turtle",
        "image": "assets/images/animals/turtle.png",
        "sound": "assets/sounds/animals/t.mp3",
        "hint": "The answer is T! Turtle starts with T!",
        "emoji": "🐢",
        "difficulty": "Medium"
    },
    {
        "letter": "T",
        "animal": "Toucan",
        "image": "assets/images/animals/toucan.png",
        "sound": "assets/sounds/animals/t.mp3",
        "hint": "The answer is T! Toucan starts with T!",
        "emoji": "🦜",
        "difficulty": "Medium"
    },
    {
        "letter": "U",
        "animal": "Unicorn",
        "image": "assets/images/animals/unicorn.png",
        "sound": "assets/sounds/animals/u.mp3",
        "hint": "The answer is U! Unicorn starts with U!",
        "emoji": "🦄",
        "difficulty": "Hard"
    },
    {
        "letter": "U",
        "animal": "Urchin",
        "image": "assets/images/animals/urchin.png",
        "sound": "assets/sounds/animals/u.mp3",
        "hint": "The answer is U! Urchin starts with U!",
        "emoji": "🦔",
        "difficulty": "Medium"
    },
    {
        "letter": "U",
        "animal": "Urial Sheep",
        "image": "assets/images/animals/urial_sheep.png",
        "sound": "assets/sounds/animals/u.mp3",
        "hint": "The answer is U! Urial Sheep starts with U!",
        "emoji": "🐏",
        "difficulty": "Hard"
    },
    {
        "letter": "V",
        "animal": "Vulture",
        "image": "assets/images/animals/vulture.png",
        "sound": "assets/sounds/animals/v.mp3",
        "hint": "The answer is V! Vulture starts with V!",
        "emoji": "🦅",
        "difficulty": "Hard"
    },
    {
        "letter": "V",
        "animal": "Viper",
        "image": "assets/images/animals/viper.png",
        "sound": "assets/sounds/animals/v.mp3",
        "hint": "The answer is V! Viper starts with V!",
        "emoji": "🐍",
        "difficulty": "Medium"
    },
    {
        "letter": "V",
        "animal": "Vicuna",
        "image": "assets/images/animals/vicuna.png",
        "sound": "assets/sounds/animals/v.mp3",
        "hint": "The answer is V! Vicuna starts with V!",
        "emoji": "🐏",
        "difficulty": "Medium"
    },
    {
        "letter": "W",
        "animal": "Whale",
        "image": "assets/images/animals/whale.png",
        "sound": "assets/sounds/animals/w.mp3",
        "hint": "The answer is W! Whale starts with W!",
        "emoji": "🐋",
        "difficulty": "Medium"
    },
    {
        "letter": "W",
        "animal": "Wolf",
        "image": "assets/images/animals/wolf.png",
        "sound": "assets/sounds/animals/w.mp3",
        "hint": "The answer is W! Wolf starts with W!",
        "emoji": "🐺",
        "difficulty": "Medium"
    },
    {
        "letter": "W",
        "animal": "Wombat",
        "image": "assets/images/animals/wombat.png",
        "sound": "assets/sounds/animals/w.mp3",
        "hint": "The answer is W! Wombat starts with W!",
        "emoji": "🐹",
        "difficulty": "Medium"
    },
    {
        "letter": "X",
        "animal": "X-ray Fish",
        "image": "assets/images/animals/x_ray_fish.png",
        "sound": "assets/sounds/animals/x.mp3",
        "hint": "The answer is X! X-ray Fish starts with X!",
        "emoji": "🐟",
        "difficulty": "Hard"
    },
    {
        "letter": "X",
        "animal": "Xerus",
        "image": "assets/images/animals/xerus.png",
        "sound": "assets/sounds/animals/x.mp3",
        "hint": "The answer is X! Xerus starts with X!",
        "emoji": "🐿️",
        "difficulty": "Medium"
    },
    {
        "letter": "X",
        "animal": "Xenops Bird",
        "image": "assets/images/animals/xenops_bird.png",
        "sound": "assets/sounds/animals/x.mp3",
        "hint": "The answer is X! Xenops Bird starts with X!",
        "emoji": "🐦",
        "difficulty": "Hard"
    },
    {
        "letter": "Y",
        "animal": "Yak",
        "image": "assets/images/animals/yak.png",
        "sound": "assets/sounds/animals/y.mp3",
        "hint": "The answer is Y! Yak starts with Y!",
        "emoji": "🐃",
        "difficulty": "Easy"
    },
    {
        "letter": "Y",
        "animal": "Yellowjacket",
        "image": "assets/images/animals/yellowjacket.png",
        "sound": "assets/sounds/animals/y.mp3",
        "hint": "The answer is Y! Yellowjacket starts with Y!",
        "emoji": "🐝",
        "difficulty": "Hard"
    },
    {
        "letter": "Y",
        "animal": "Yabby Lobster",
        "image": "assets/images/animals/yabby_lobster.png",
        "sound": "assets/sounds/animals/y.mp3",
        "hint": "The answer is Y! Yabby Lobster starts with Y!",
        "emoji": "🦞",
        "difficulty": "Hard"
    },
    {
        "letter": "Z",
        "animal": "Zebra",
        "image": "assets/images/animals/zebra.png",
        "sound": "assets/sounds/animals/z.mp3",
        "hint": "The answer is Z! Zebra starts with Z!",
        "emoji": "🦓",
        "difficulty": "Medium"
    },
    {
        "letter": "Z",
        "animal": "Zebu Cow",
        "image": "assets/images/animals/zebu_cow.png",
        "sound": "assets/sounds/animals/z.mp3",
        "hint": "The answer is Z! Zebu Cow starts with Z!",
        "emoji": "🐂",
        "difficulty": "Hard"
    },
    {
        "letter": "Z",
        "animal": "Zorilla Skunk",
        "image": "assets/images/animals/zorilla_skunk.png",
        "sound": "assets/sounds/animals/z.mp3",
        "hint": "The answer is Z! Zorilla Skunk starts with Z!",
        "emoji": "🦨",
        "difficulty": "Hard"
    }
]
