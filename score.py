import sys
import pandas as pd

# Import letter frequency table
freq_df = pd.read_csv("freq.csv")
freq_df['letter'] = freq_df['letter'].astype('str')
freq_df['freq'] = freq_df['freq'].astype('float')

freq = {}
for index, row in freq_df.iterrows():
    freq[row['letter'].lower()] = row['freq']

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
        print("   " + str(key) + ": " + str(val))