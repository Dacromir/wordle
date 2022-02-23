import pandas as pd
import json, shutil, math, sys

### A script to solve wordle automatically

# Load wordle word dictionary from file
wdict = []
full_dict = []
with open('dict.json') as json_file:
    wdict = json.load(json_file)

full_dict = wdict.copy()
mode = "hard"
if len(sys.argv) > 1:
    if sys.argv[1] == "easy":
        mode = "easy"

size = len(wdict)
matches = {}

# Generate the result of a guess for a given word
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

# Generate all possible matches for remaining words
def gen_matches():
    matches = {}
    if mode == "easy":
        for word in full_dict:
            matches[word] = {}
            for guess in wdict:
                matches[word][guess] = gen_pattern(word, guess)
    else:
        for word in wdict:
            matches[word] = {}
            for guess in wdict:
                matches[word][guess] = gen_pattern(word, guess)
    
    return matches

# Generate expected bits of entropy for a given word
def gen_score(word):
    patterns = {}

    # Count numbers of each pattern
    for w in wdict:
        p = matches[word][w]
        if p in patterns:
            patterns[p] += 1
        else:
            patterns[p] = 1

    score = 0

    # Sum up bits of entropy
    for p, n in patterns.items():
        score += (n/size) * math.log((size/n),2)
    
    return score

def gen_recommendation():
    # Create dataframe
    if len(wdict) == 1:
        return wdict[0]
    
    if mode == "easy":
        words = pd.DataFrame(full_dict, columns = ['word'])
    else:
        words = pd.DataFrame(wdict, columns = ['word'])

    # Apply Score
    words['score'] = words.apply(lambda x: gen_score(x['word']), axis=1)
    words = words.sort_values(by=['score'], ascending=False)
    # print(words.head(10))

    # Output best word
    return words.at[words['score'].idxmax(), 'word']

# Filter out words that are no longer valid
def filter_dict(guess, result):
    new_dict = []
    for word in wdict:
        pattern = gen_pattern(word, guess)
        if pattern == result:
            new_dict.append(word)
    return new_dict

print("Result key: \"G\" = Green, \"Y\" = Yellow, \"-\" = Gray\n")
print("Words remaining: " + str(size))
guess = input("Guess:  ").lower()
result = input("Result: ").upper()

wdict = filter_dict(guess,result)
matches = gen_matches()
size = len(wdict)

while True:
    if size <= 100:
        print("\nWords remaining: " + str(size))
        row_count = 0
        row_max = 10
        row = ""
        for n in range(size):
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
            
            if n == (size - 1) and row_count > 0:
                print(row)
    else:
        print("\nWords remaining: " + str(size))

    next_guess = gen_recommendation()
    print("Recommended guess: " + next_guess.upper())

    guess = input("Guess:  ").lower()
    if guess == "":
        break
    result = input("Result: ").upper()

    if result == "GGGGG":
        print("\nCongratulations!")
        break

    wdict = filter_dict(guess,result)
    matches = gen_matches()
    size = len(wdict)
    
