import pandas as pd
import json, shutil

## Utility to create a frequency chart from a given word dictionary

# Load wordle word dictionary from file
wdict = {}
with open('dict.json') as json_file:
    wdict = json.load(json_file)

freq = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, "m": 0,
        "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0}

# Generate word frequency list
for word in wdict:
    for char in word:
        freq[char] += 1

total = 0
for val in freq.values():
    total += val

for char, val in freq.items():
    new_val = val / total * 100
    new_val = float(format(new_val, '.2f'))
    freq[char] = new_val

with open('freq.json', 'w') as json_file:
    json_file.write(json.dumps(freq))