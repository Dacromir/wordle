import pandas as pd
import json, shutil, math

### A script to determine which words have the highest expected value on turn 1 (Warning: Takes a lot of CPU and RAM)

wdict = []
full_dict = []
matches = {}

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
        if guess[n] in chars:
            if chars[guess[n]] > 0:
                pattern = pattern[:n] + "Y" + pattern[(n+1):]
                chars[guess[n]] -= 1
        
    return pattern

def gen_score(word):
    patterns = {}
    for p in matches[word].values():
        if p in patterns:
            patterns[p] += 1
        else:
            patterns[p] = 1
    
    score = 0
    size = len(wdict)
    for p in patterns.values():
        score += (p/size) * (math.log((size/p), 2))
    
    return score

if __name__ == "__main__":
    # Load wordle word dictionary from file
    with open('dict.json') as json_file:
        wdict = json.load(json_file)
        full_dict = wdict

    # Generate match for each word
    print("Generating matches")
    for word in wdict:
        print(str(word), end="\r")
        matches[word] = {}
        for guess in wdict:
            matches[word][guess] = gen_pattern(word, guess)
    
    # Create a dataframe for the wordlist
    words = pd.DataFrame(wdict, columns = ['word'])

    # Add a score column to words
    print("Generating scores")
    words['score'] = words.apply(lambda x: gen_score(x['word']), axis=1)

    # Sort words by highest score
    print("Scores generated: ")
    words = words.sort_values(by=['score'], ascending=False)
    print(words.head(25))

    # Create a JSON output
    print("Creating JSON")
    word_dict = words.to_dict(orient='records')
    output = {}
    for d in word_dict:
        output[d["word"]] = round(d["score"], 3)

    print("Writing file")
    with open('scores.json', 'w') as json_output:
        json_output.write(json.dumps(output, indent=3))
    
    print("Done!")

