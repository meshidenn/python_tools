#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import __future__
import sys
from argparse import ArgumentParser

def parser():
    usage = 'Usage: python {} [--input] [--output] [--begin_id]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('-i','--input',
                                required=True,
                                type=str,
                                help="input file for insert id(necessary option)")
    argparser.add_argument('-o','--output',
                                required=True,
                                type=str,
                                help="output file name(necessary option)")
    argparser.add_argument('-b','--begin_id',
                                type=int,
                                default=0,
                                help="begining id(default 0)")
    args = argparser.parse_args()
    return args
                                

def main(open_fn,out_fn,j):
    with open(open_fn,'r') as f:
        for i,line in enumerate(f):
            char = str(j) + '\t' + line
            if i == 0:
                with open(out_fn,'w') as g:
                    print(char, end="",file=g)
            else:
                with open(out_fn,'a+') as g:
                    print(char, end="",file=g)

            j += 1


if __name__ == '__main__':
    args = parser()
    open_fn = args.input
    out_fn = args.output
    j = args.begin_id
    main(open_fn, out_fn, j)
