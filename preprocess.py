import nltk
import string
from unicodedata import normalize
import numpy as np
import re
import pickle
from tqdm import tqdm
import pandas as pd
import argparse

class PreprocessData:
    def __init__(self, path):
        self.path = path
        self.load_data()

    def load_data(self):
        with open(self.path, mode='rt', encoding='utf-8') as f:
            self.text = f.read().strip().split('\n')

        self.text_pairs = []
        for line in self.text:
            self.text_pairs.append(line.split('\t'))

    def clean_text(self):
        cleaned = []
        re_print = re.compile('[^%s]' % re.escape(string.printable))

        table = str.maketrans('', '', string.punctuation)
        for pair in self.text_pairs:
            clean_pair = []
            for line in pair:
                line = normalize('NFD', line).encode('ascii', 'ignore')
                line = line.decode('UTF-8')
                line = line.split(' ')

                line = [word.lower() for word in line]
                line = [word.translate(table) for word in line]
                line = [re_print.sub('', word) for word in line]
                line = [word for word in line if word.isalpha()]

                clean_pair.append(' '.join(line))

            cleaned.append(clean_pair)

        return cleaned

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', '-d', help='Path to .txt file downloaded from http://www.manythings.org/anki/', required=True)
parser.add_argument('--language_1', '-l1', help='Language-1 name | Default: english', default='english')
parser.add_argument('--language_2', '-l2', help='Language-2 name', required=True)
parser.add_argument('--save_file', '-s', help='Name of CSV file to be generated | Default: dataset.csv', default='dataset.csv')
args = parser.parse_args()

preprocess = PreprocessData(args.dataset)
cleaned_text = preprocess.clean_text()
english = []
german = []

for pair in tqdm(cleaned_text):
    english.append(pair[0])
    german.append(pair[1])

df = pd.DataFrame([english, german])
df = df.transpose()
df.columns = [args.language_1, args.language_2]
print(df.head())
df.to_csv(args.save_file)
df = df.sample(frac=1).reset_index(drop=True)
df = df.sample(frac=1).reset_index(drop=True)
