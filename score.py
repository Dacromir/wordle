import sys, shutil, json
import pandas as pd

# Import letter frequency table
freq = {}
with open('freq.json') as f:
    freq = json.load(f)

# Function to generate a score for a given word
def gen_score(word):
    score = 0
    chars = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
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

        # Save values
        score += char_score
        chars[slot] = {"letter": char, "score": char_score}
        
        # Next slot
        slot += 1
    
    output = {
        'total': score,
        'chars': chars
    }
    return output


# Give each word in arguments a score
words = sys.argv[1:]
for word in words:
    word = word.lower()

    score_dict = gen_score(word)

    print(word.upper() + " word score: " + format(score_dict['total'], '.1f'))
    for key, char in score_dict['chars'].items():
        print("   " + str(char["letter"]) + ": " + format(char["score"], '.1f'))



## WORD SCORE MATH ##
# g = odds of green in slot
# y = odds of yellow in slot
# x = odds of grey in slot
# c = odds of character being in word

# c = y + g
# x + c = 1

# w = word score
# w = (g * (1-g) + (y * (1-y)) + (x * (1-x))
# w = (g * (1-g)) + ((c-g) * (1-c+g)) + ((1-c) * c)
# w = g -g^2 +c -c^2 +cg -g +cg -g^2 +c -c^2
# w = 2cg +2c -2g^2 -2c^2