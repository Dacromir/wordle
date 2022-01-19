import pandas as pd

# Import word dictionary
words = pd.read_csv("words.txt", sep=" ", header=None, names=['word'])
words['word'] = words['word'].astype('str').str.lower()

# Import letter frequency table
freq_df = pd.read_csv("freq.csv")
freq_df['letter'] = freq_df['letter'].astype('str')
freq_df['freq'] = freq_df['freq'].astype('float')

freq = {}
for index, row in freq_df.iterrows():
    freq[row['letter'].lower()] = row['freq']

# Filter word list to valid wordle inputs
words = words.loc[
    (words['word'].str.fullmatch('[a-zA-Z]{5}'))
]

# Function to generate a score for a word
def gen_score(input):
    score = 0
    chars = []
    for char in input:
        if char not in chars:
            score += freq[char]
            chars.append(char)
    return score

# Add a score column to words
words['score'] = words.apply(lambda x: gen_score(x['word']), axis=1)

# Sort words by highest score
words = words.sort_values(by=['score'], ascending=False)

print(words.head(20))


