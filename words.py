import pandas as pd
import json, shutil


# Load wordle word dictionary from file
wdict = {}
with open('dict.json') as json_file:
    wdict = json.load(json_file)

# Load word frequency dictionary from file
freq = {}
with open('freq.json') as json_file:
    freq = json.load(json_file)

