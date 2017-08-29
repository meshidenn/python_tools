# -*- coding:utf-8 -*-

import pandas as pd
import datetime as dt
import csv
#import pdb;pdb.set_trace()
from argparse import ArgumentParser
from pandas import Series, DataFrame

# input parser
def parser():
    usage = 'Usate: python {} [--input] [--truth file]'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('-i','--input',required=True,type=str,
                           help='input fill annotation file')
    argparser.add_argument('-t','--truth',required=True,type=str,
                           help='input truth file')
    args = argparser.parse_args()
    return args

def is_true(df, true_keys):
    user_id = true_keys[1]['userId']
    tmp  = df[df.userId == user_id]['tweetTime']
    tweet_time_tk = true_keys[1]['tweetTime']
    if tweet_time_tk in list(tmp):
        return True
    else:
        return False        

def main(arg):
    infile = arg.input
    truefile = arg.truth
    count = 0

    fa = pd.read_csv(infile, encoding='cp932',
                     skiprows=1, parse_dates=['tweetTime'])
    ft = fa[fa.annotation == True]
    tmp = pd.read_csv(truefile,
                      names=['userId','tweetTime'],
                      parse_dates=['tweetTime'])
    tu = tmp['userId'].str.strip('@')
    tt = tmp['tweetTime']
    tdt = pd.concat([tu, tt], axis=1)
    for t in tdt.iterrows():
        if is_true(ft,t):
            count += 1

    print(count)

if __name__ == '__main__':
    arg = parser()
    main(arg)

