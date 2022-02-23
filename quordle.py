import pandas as pd
import json, shutil, math, sys


# Load wordle word dictionary from file
wdict1 = []
wdict2 = []
wdict3 = []
wdict4 = []
full_dict = []
answers = ["", "", "", ""]
with open('dict.json') as json_file:
    wdict1 = json.load(json_file)

full_dict = wdict1.copy()
wdict2 = wdict1.copy()
wdict3 = wdict1.copy()
wdict4 = wdict1.copy()

matches = {}
size = len(wdict1) + len(wdict2) + len(wdict3) + len(wdict4)



def gen_pattern(word, guess):
    chars = {}
    pattern = "-----"
    for char in word:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1

    # Green pass
    for n in range(5):
        if word[n] == guess[n]:
            pattern = pattern[:n] + "G" + pattern[(n+1):]
            chars[guess[n]] -= 1
    
    # Yellow pass
    for n in range(5):
        if pattern[n] == "-" and guess[n] in chars:
            if chars[guess[n]] > 0:
                pattern = pattern[:n] + "Y" + pattern[(n+1):]
                chars[guess[n]] -= 1
        
    return pattern

def gen_matches():
    matches = {}
    combined_dict = list(set(wdict1 + wdict2 + wdict3 + wdict4))
    for word in full_dict:
        matches[word] = {}
        for guess in combined_dict:
            matches[word][guess] = gen_pattern(word, guess)
    
    return matches

def gen_score(word):
    patterns = {}

    # Count numbers of each pattern
    for wdict in (wdict1, wdict2, wdict3, wdict4):
        for w in wdict:
            p = matches[word][w]
            if p in patterns:
                patterns[p] += 1
            else:
                patterns[p] = 1

    score = 0

    # Sum up bits of entropy
    for p, n in patterns.items():
        p_bits = (n/size) * math.log((size/n),2)
        if p == "GGGGG":
            p_bits *= 2 # Hacky but it should work
        score += p_bits
    
    return score

def gen_recommendation():
    # Create dataframe
    if len(wdict1) == 1:
        return wdict1[0]
    elif len(wdict2) == 1:
        return wdict2[0]
    elif len(wdict3) == 1:
        return wdict3[0]
    elif len(wdict4) == 1:
        return wdict4[0]
    
    words = pd.DataFrame(full_dict, columns = ['word'])

    # Apply Score
    words['score'] = words.apply(lambda x: gen_score(x['word']), axis=1)
    words = words.sort_values(by=['score'], ascending=False)
    # print(words.head(10))

    # Output best word
    return words.at[words['score'].idxmax(), 'word']

def filter_dict(start_dict, guess, result):
    new_dict = []
    for word in start_dict:
        pattern = gen_pattern(word, guess)
        if pattern == result:
            new_dict.append(word)
    return new_dict

def print_dict(wdict, dict_label):
    if len(wdict) > 0:
        print("\n" + dict_label + ": Words remaining: " + str(len(wdict)))

    # Print out remaining words (if less than 250)
    if len(wdict) <= 250:
        row_count = 0
        row_max = 10
        row = ""
        for n in range(len(wdict)):
            if row_count == 0:
                row = "    " + wdict[n]
                row_count = 1
            elif row_count < (row_max - 1):
                row += ", " + wdict[n]
                row_count += 1
            elif row_count == (row_max - 1):
                row += ", " + wdict[n]
                print(row)
                row = ""
                row_count = 0
            
            if n == (len(wdict) - 1) and row_count > 0:
                print(row)


print("Result key: \"G\" = Green, \"Y\" = Yellow, \"-\" = Gray\n")
print ("Words remaining: " + str(len(wdict1)))
guess = input("Guess:    ").lower()
result1 = input("Result 1: ").upper()
result2 = input("Result 2: ").upper()
result3 = input("Result 3: ").upper()
result4 = input("Result 4: ").upper()

if result1 == "GGGGG":
    wdict1 = []
    answers[0] = guess
    result1 = ""
elif result1 != "":
    wdict1 = filter_dict(wdict1, guess, result1)
if result2 == "GGGGG":
    wdict2 = []
    answers[1] = guess
    result2 = ""
elif result2 != "":
    wdict2 = filter_dict(wdict2, guess, result2)
if result3 == "GGGGG":
    wdict3 = []
    answers[2] = guess
    result3 = ""
elif result3 != "":
    wdict3 = filter_dict(wdict3, guess, result3)
if result4 == "GGGGG":
    wdict4 = []
    answers[3] = guess
    result4 = ""
elif result4 != "":
    wdict4 = filter_dict(wdict4, guess, result4)
matches = gen_matches()
size = len(wdict1) + len(wdict2) + len(wdict3) + len(wdict4)

while True:
    print_dict(wdict1, "Set 1")
    print_dict(wdict2, "Set 2")
    print_dict(wdict3, "Set 3")
    print_dict(wdict4, "Set 4")

    next_guess = gen_recommendation()
    print("\nRecommended guess: " + next_guess.upper())

    guess = input("Guess:    ").lower()
    if guess == "":
        break
    
    if len(wdict1) > 0:
        result1 = input("Result 1: ").upper()
    else:
        print("Set 1:    " + str(answers[0]).upper())

    if len(wdict2) > 0:
        result2 = input("Result 2: ").upper()
    else:
        print("Set 2:    " + str(answers[1]).upper())

    if len(wdict3) > 0:
        result3 = input("Result 3: ").upper()
    else:
        print("Set 3:    " + str(answers[2]).upper())
    
    if len(wdict4) > 0:
        result4 = input("Result 4: ").upper()
    else:
        print("Set 4:    " + str(answers[3]).upper())

    if result1 == "GGGGG":
        wdict1 = []
        answers[0] = guess
        result1 = ""
    elif result1 != "":
        wdict1 = filter_dict(wdict1, guess, result1)
    if result2 == "GGGGG":
        wdict2 = []
        answers[1] = guess
        result2 = ""
    elif result2 != "":
        wdict2 = filter_dict(wdict2, guess, result2)
    if result3 == "GGGGG":
        wdict3 = []
        answers[2] = guess
        result3 = ""
    elif result3 != "":
        wdict3 = filter_dict(wdict3, guess, result3)
    if result4 == "GGGGG":
        wdict4 = []
        answers[3] = guess
        result4 = ""
    elif result4 != "":
        wdict4 = filter_dict(wdict4, guess, result4)

    matches = gen_matches()
    size = len(wdict1) + len(wdict2) + len(wdict3) + len(wdict4)
    if size == 0:
        print("\nANSWERS:")
        print("Set 1:    " + str(answers[0]).upper())
        print("Set 2:    " + str(answers[1]).upper())
        print("Set 3:    " + str(answers[2]).upper())
        print("Set 4:    " + str(answers[3]).upper())
        print("\nCongratulations!")
        break
    
