import pandas as pd
import json, shutil

## Utility to create a frequency chart from a given word dictionary

# Load wordle word dictionary from file
wdict = {}
with open('dict.json') as json_file:
    wdict = json.load(json_file)

freq = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, "m": 0,
        "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0}

# Generate sub-dictionaries
for key in freq.keys():
    freq[key] = {
        "count": 0,
        "slot": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        "freq": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    }

# Word count
wcount = len(wdict)

# Generate word frequency list
for word in wdict:
    slot = 1
    char_count = {}
    for char in word:
        freq[char]["slot"][slot] += 1
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
        slot += 1
    
    for char, count in char_count.items():
        freq[char]["count"] += 1
        freq[char]["freq"][count] += 1
  
for char in freq.keys():
    freq[char]["freq+"] = {
        1: freq[char]["freq"][1] + freq[char]["freq"][2] + freq[char]["freq"][3] + freq[char]["freq"][4] + freq[char]["freq"][5],
        2: freq[char]["freq"][2] + freq[char]["freq"][3] + freq[char]["freq"][4] + freq[char]["freq"][5],
        3: freq[char]["freq"][3] + freq[char]["freq"][4] + freq[char]["freq"][5],
        4: freq[char]["freq"][4] + freq[char]["freq"][5],
        5: freq[char]["freq"][5],
    }

# Add word count to dictionary
freq["count"] = wcount

# Save fequency dict to JSON
with open('freq.json', 'w') as json_file:
    json_file.write(json.dumps(freq, indent=4))