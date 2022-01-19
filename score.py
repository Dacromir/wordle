import sys, shutil, json
import pandas as pd

# Import letter frequency table
freq = {}
with open('freq.json') as f:
    freq = json.load(f)

words = sys.argv[1:]
for word in words:
    word = word.lower()

    score = 0
    chars = {}

    for char in word:
        if not char in chars:
            char_score = freq[char]
            chars[char] = char_score
            score += char_score

    print(word.upper() + " word score: " + format(score, '.1f'))
    for key, val in chars.items():
        print("   " + str(key) + ": " + format(val, '.1f'))