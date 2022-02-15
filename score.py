import sys, shutil, json
import pandas as pd

# Load wordle word dictionary from file
wdict = {}
with open('dict.json') as json_file:
    wdict = json.load(json_file)

# Load word frequency dictionary from file
freq = {}
with open('freq.json') as json_file:
    freq = json.load(json_file)

# Create a dataframe for the wordlist
words = pd.DataFrame(wdict, columns = ['word'])
words['score'] = 1

# Function to generate a score for a given word
def gen_score(word):
    score = 0
    words['score'] = 1
    chars = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    char_count = {}
    slot = 1

    for char in word:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
        
        # TODO: Handle odds of yellow for when there are multiple copies of a letter in the word
        n = freq["count"]                              # Total number of words in dictionary
        w = freq[char]["freq+"][str(char_count[char])] # Number of words containing this character in any slot
        g = freq[char]["slot"][str(slot)] / n          # Odds of green in slot
        y = (w - freq[char]["slot"][str(slot)]) / n    # Odds of yellow in slot
        x = (n - w) / n                                # Odds of grey in slot

        print("Char: " + str(char) + str({"n": n, "w": w, "g": g, "y": y, "x": x}))

        # Average number of possible words eliminated by this character: 
        char_score = ((g/n) * (n-g)) + ((y/n) * (n-y)) + ((x/n) * (n-x))
        chars[slot] = {"letter": char, "score": char_score}

        scores = []
        for index, row in words.iterrows():
            row_score = 1
            
            if row['word'][slot-1] != char: # Eliminated by green
                row_score -= g
            if row['word'].count(char) < char_count[char]: # Eliminated by yellow
                row_score -= y
            if row['word'].count(char) >= char_count[char]: # Eliminated by gray
                row_score -= x
            
            scores.append(row_score)
        
        words['score'] *= scores
        # print(words)
        
        # Next slot
        slot += 1
    
    output = {
        'total': score,
        'chars': chars
    }
    return output


# Give each word in arguments a score
score_dict = gen_score('aahed')
words = sys.argv[1:]
for word in words:
    word = word.lower()

    score_dict = gen_score(word)

    print(word.upper() + " word score: " + format(score_dict['total'], '.1f'))
    for key, char in score_dict['chars'].items():
        print("   " + str(char["letter"]) + ": " + format(char["score"], '.1f'))