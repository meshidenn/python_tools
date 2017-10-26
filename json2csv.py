# -*- coding:utf-8 -*-

import csv
import json
import sys
#import pdb;pdb.set_trace()
from argparse import ArgumentParser
from pandas import Series, DataFrame

def parser():
    use = 'Usage: python {} [--input] [--output] [--escape]'.format(__file__)
    argparser = ArgumentParser(usage=use)
    argparser.add_argument('-i','--input',
                           required=True, type=str,
                           help='input json')
    argparser.add_argument('-o','--output',
                           required=True, type=str,
                           help='output csv')
    argparser.add_argument('-e','--escape',
                           type=int, default=0,
                           help='0:QUOTE_MINIMAL, 1:QUOTE_ALL, 2:QUOTE_NONNUMERIC, 3:QUOTE_NONE')
    args = argparser.parse_args()
    return args

def main(arg):
    injson = arg.input
    outcsv = arg.output
    es =  arg.escape
    jsons = load_json(injson)

    out_csv(outcsv, jsons, es)
    


def load_json(infile):
    out = []
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line.strip())
            out.append(d)

    return out

def out_csv(outcsv, jsons, es):
    header = jsons[0].keys()
    
    with open(outcsv, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=es)
        writer.writerow(header)
        for j in jsons:
            writer.writerow(j.values())
        



if __name__ == '__main__':
    arg = parser()
    main(arg)
