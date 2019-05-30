import sqlite3
import sys
import os
from collections import namedtuple


# define class like object
Word = namedtuple('Word', 'wordid lang lemma pron pos')
Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')
Synset = namedtuple('Synset', 'synset pos name src')


def get_all_words(conn, language):
    cur = conn.execute("select wordid, lemme from word where lang=?", (language, ))
    return [Word(*row) for row in cur]


def get_Synsets(conn):
    cur = conn.execute("select * from synset")
    return [Synset(*row) for row in cur]


def get_synonyms_from_senses(conn, synset, language):
    cur = conn.execute('select * from sense where synset=? and lang = ?', (synset, language))
    return [Sense(*row) for row in cur]


def get_lemma(conn, synonym, language):
    cur = conn.execute("select lemma from word where wordid = ? and lang = ?", (synonym.wordid, language))
    return [row[0] for row in cur]


def get_synonyms(conn, synsets, language):
    synset2synonym = dict()
    syn_set = set()
    for synset in synsets:
        senses = get_synonyms_from_senses(conn, synset.synset, language)
        lemmas = []
        for s in senses:
            lemma = get_lemma(conn, s, language)
            lemmas.extend(lemma)

        if len(lemmas) > 1:
            if synset.name not in synset2synonym:
                synset2synonym[synset.name] = lemmas
            else:
                # in principle, synset.name is unique so this will not run.
                synset2synonym[synset.name].extend(lemmas)

    for k, synonyms in synset2synonym.items():
        print(k, synonyms)
        for i, sy1 in enumerate(synonyms):
            if i > len(synonyms) - 1:
                break
            for sy2 in synonyms[i+1:]:
                if sy1 != sy2:
                    syn_set.add((sy1, sy2))
                
    return syn_set
    

def get_hyper(conn, language):
    cor_hype = conn.execute("select synset1, synset2 from synlink where link = 'hype'")
    hypes = set()
    for row in cor_hype:
        senses_hype1 = get_synonyms_from_senses(conn, row[0], language)
        senses_hype2 = get_synonyms_from_senses(conn, row[1], language)
        lemma_hype1 = []
        lemma_hype2 = []
        for sh1 in senses_hype1:
            lemma = get_lemma(conn, sh1, language)
            lemma_hype1.extend(lemma)
        for sh2 in senses_hype2:
            lemma = get_lemma(conn, sh2, language)
            lemma_hype2.extend(lemma)

        if len(lemma_hype1) * len(lemma_hype2):
            print(row[0], lemma_hype1, row[1], lemma_hype2)
            for lh1 in lemma_hype1:
                for lh2 in lemma_hype2:
                    if lh1 != lh2:
                        hypes.add((lh1, lh2))

    return hypes


def save(folder, synonyms, hypes):
    if not os.path.exists(folder):
        os.makedirs(folder)
                          
    out_synonym = os.path.join(folder, 'synonyms.txt')
    out_hype = os.path.join(folder, 'hypernym.txt')
    with open(out_synonym, 'w') as f:
        for syn in synonyms:
            print(' '.join(syn), file=f)
            
    with open(out_hype, 'w') as f:
        for hype in hypes:
            print(' '.join(hype), file=f)
        

def main():
    try:
        db = sys.argv[1]
        language = sys.argv[2]
        outdir = sys.argv[3]
    except Exception:
        print("use default path")
        db = os.path.join("data", "language", "wnjpn.db")
        language = "jpn"
        outdir = "syn_hype"

    conn = sqlite3.connect(db)
    synsets = get_Synsets(conn)
    print("start getting synonyms")
    synonyms = get_synonyms(conn, synsets, language)
    print("start getting hypers")
    hypers = get_hyper(conn, language)
    print("saving")
    save(outdir, synonyms, hypers)


if __name__ == "__main__":
    main()
