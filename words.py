import pandas as pd
import json, shutil


# Load wordle word dictionary from file
wdict = {}
with open('dict.json') as json_file:
    wdict = json.load(json_file)
print("Word dictionary loaded")

# Load word frequency dictionary from file
freq = {}
with open('freq.json') as json_file:
    freq = json.load(json_file)
print("Word frequency loaded")

# Load match file file
match = {}
with open('match.json') as json_file:
    match = json.load(json_file)
print("Match file loaded")

# Create a dataframe for the wordlist
words = pd.DataFrame(wdict, columns = ['word'])

# Function to generate a score for a word
def gen_score(word):
    score = 0
    char_count = {}
    slot = 1

    for char in word:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
        
        n = freq["count"]                              # Total number of words in dictionary
        w = freq[char]["freq+"][str(char_count[char])] # Number of words containing this character in any slot
        g = freq[char]["slot"][str(slot)]              # Words with green in slot
        y = w - g                                      # Words with yellow in slot
        x = n - w                                      # Words with grey in slot

        # Average number of possible words eliminated by this character: 
        char_score = ((g/n) * (n-g)) + ((y/n) * (n-y)) + ((x/n) * (n-x))
        
        # Convert to percentage
        char_score = char_score / n * 100

        score += char_score
        slot += 1
    
    return round(score, 2)

# Add a score column to words
words['score'] = words.apply(lambda x: gen_score(x['word']), axis=1)

# Sort words by highest score
words = words.sort_values(by=['score'], ascending=False)
print(words.head(25))