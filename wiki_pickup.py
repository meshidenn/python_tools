from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import os
import re
import MeCab
import argparse
import numpy as np
import json


class TargetDocs(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.file_names = []
        wakati = MeCab.Tagger("-O wakati")
        wakati.parse("")
        self.tokenizer = wakati
 
    def __iter__(self):
        for root, dirs, files in os.walk(self.dirname, followlinks=True):
            for filename in files:
                file_path = root + '/' + filename
                print(file_path)
                wakati_lines = ""
                with open(file_path) as f:
                    for line in f:
                        sline = line.strip()
                        if sline == "":
                            continue
                        wakati_lines += " " + self.tokenizer.parse(sline).strip()
    
                        self.file_names.append(file_path)
                yield wakati_lines


class WikiDocs(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.file_names = []
        wakati = MeCab.Tagger("-O wakati")
        wakati.parse("")
        self.tokenizer = wakati
 
    def __iter__(self):
        for root, dirs, files in os.walk(self.dirname, followlinks=True):
            for filename in files:
                file_path = root + '/' + filename
                print(file_path)
                wakati_lines = ""
                with open(file_path) as f:
                    for line in f:
                        sline = line.strip()
                        if sline == "":
                            continue
                        jline = json.loads(sline)
                        rline = jline['text']
                 
                        wakati_lines += " " + self.tokenizer.parse(rline).strip()
                        self.file_names.append((file_path, jline['id']))
                        yield wakati_lines


def main(args):
    wiki_path = args.input_wiki
    target_path = args.input_target
    output = args.output

    wiki_docs = WikiDocs(wiki_path)
    target_docs = TargetDocs(target_path)
    count = CountVectorizer()
    tfidf = TfidfTransformer(use_idf=True, smooth_idf=True)
    wiki_tfidf = tfidf.fit_transform(count.fit_transform(wiki_docs))
    target_tfidf = tfidf.transform(target_docs)
    similarity = cosine_similarity(target_tfidf, wiki_tfidf)
    mms = MinMaxScaler()
    sim_norm = mms.fit_traisform(similarity)
    threshold = 0.9 * (1 - mms.min_)
    pickup = np.where(sim_norm > threshold)
    all_file_names = wiki_docs.file_names
    filename = set()
    for pu in pickup:
        filename.add(all_file_names[pu[1]])

    if args.random:
        n = len(all_file_names)
        rand_pickup = np.random.randint(0, n, int(0.1*n))
        for rpu in rand_pickup:
            filename.add(all_file_names[rpu])

    with open(output, 'w') as f:
        for fn in filename:
            print(fn, file=f)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='train w2v with gensim')
    parser.add_argument('-it', '--input_target', help='set input target corpus dir')
    parser.add_argument('-iw', '--input_wiki', help='set input dir')
    parser.add_argument('-o', '--output', help='set output filename')
    parser.add_argument('--random', help='add randomly picking up docs')

    args = parser.parse_args()

    main(args)

