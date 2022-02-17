import pandas as pd
import json, shutil, math


# Load wordle word dictionary from file
wdict = []
with open('dict.json') as json_file:
    wdict = json.load(json_file)

size = len(wdict)
matches = {}

def gen_pattern(word, input):
    chars = {}
    pattern = "-----"
    for char in word:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1

    # Green pass
    for n in range(5):
        if word[n] == input[n]:
            pattern = pattern[:n] + "G" + pattern[(n+1):]
            chars[input[n]] -= 1
    
    # Yellow pass
    for n in range(5):
        if pattern[n] == "-" and input[n] in chars:
            if chars[input[n]] > 0:
                pattern = pattern[:n] + "Y" + pattern[(n+1):]
                chars[input[n]] -= 1
        
    return pattern

def gen_matches():
    matches = {}
    for word in wdict:
        matches[word] = {}
        for input in wdict:
            matches[word][input] = gen_pattern(word, input)
    
    return matches

def filter_dict(guess, result):
    new_dict = []
    for word in wdict:
        pattern = gen_pattern(word, guess)
        if pattern == result:
            new_dict.append(word)
    return new_dict

print ("Words remaining: " + str(size))
guess = input("Guess:  ").lower()
result = input("Result: ").upper()

wdict = filter_dict(guess,result)
matches = gen_matches()
size = len(wdict)

for n in range(5):
    print("\nWords remaining: " + str(size))
    row_count = 0
    row_max = 15
    row = ""
    for n in range(size):
        if row_count == 0:
            row = "    " + wdict[n]
            row_count = 1
        elif row_count < (row_max - 1):
            row += " " + wdict[n]
            row_count += 1
        elif row_count == (row_max - 1):
            row += " " + wdict[n]
            print(row)
            row = ""
            row_count = 0
        
        if n == (size - 1) and row_count > 0:
            print(row)

    guess = input("\nGuess:  ").lower()
    if guess == "":
        break
    result = input("Result: ").upper()

    if result == "GGGGG":
        print("\nCongratulations!")
        break

    wdict = filter_dict(guess,result)
    size = len(wdict)
    
