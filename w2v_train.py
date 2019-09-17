# -*- coding: utf-8 -*-
# Author: Pan Yang (panyangnlp@gmail.com)
# Copyright 2017 @ Yu Zhen
 
import gensim
import logging
import multiprocessing
import os
import re
import MeCab
import argparse

from pathlib import Path
from nltk import tokenize
from time import time
 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
 
 
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext
 
 
class MySentences(object):
    def __init__(self, dirname, lang):
        self.dirname = dirname
        self.lang = lang
        if 'en' in lang.lower():
            self.tokenizer = tokenize
        elif 'ja' in lang.lower() or 'jp' in lang.lower():
            wakati = MeCab.Tagger("-O wakati")
            wakati.parse("")
            self.tokenizer = wakati
        else:
            raise('you can only set en or (ja or jp) as lang')
 
    def __iter__(self):
        for root, dirs, files in os.walk(self.dirname, followlinks=True):
            for filename in files:
                file_path = root + '/' + filename
                print(file_path)
                for line in open(file_path):
                    sline = line.strip()
                    if sline == "":
                        continue
                    rline = cleanhtml(sline)
                    if 'en' in self.lang:
                        tokenized_line = ' '.join(self.tokenizer.sent_tokenize(rline))
                        tokens_line = [word for word in
                                       tokenized_line.lower().split() if word.isalpha()]
                    elif 'ja' in lang.lower() or 'jp' in lang.lower():
                        tokens_line = self.tokenizer.parse(rline).strip().split(" ")
                        
                    yield tokens_line
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train w2v with gensim')
    parser.add_argument('-i', '--input', help='set input dir')
    parser.add_argument('-o', '--output', help='set output filename')
    parser.add_argument('-l', '--lang', help='set language (english or japanese)')

    args = parser.parse_args()
    
    data_path = args.input
    lang = args.lang
    
    begin = time()
 
    sentences = MySentences(data_path, lang)
    model = gensim.models.Word2Vec(sentences,
                                   size=200,
                                   window=10,
                                   min_count=10,
                                   iter=50,
                                   workers=multiprocessing.cpu_count())
    # model.build_vocab(sentences)
    # sentences = MySentences(data_path, lang)
    # model.train(sentences)

    output = Path(args.output)
    if not(output.parent.exists()):
        output.mkdir(parents=True, exist_ok=True)
        
    model.save(args.output)
    # model.wv.save_word2vec_format('w2vformat_' + args.output,
    #                               'vocabulary_' + args.output,
    #                               binary=False)
 
    end = time()
    print("Total procesing time: %d seconds" % (end - begin))
