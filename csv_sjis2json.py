import json
import sys
import codecs
import argparse

def argument():
    parser = argparse.ArgumentParser(description='convert csv to jsonl')
    parser.add_argument('--input','-i')
    parser.add_argument('--output','-o')
    parser.add_argument('--encoding','-e')

    args = parser.parse_args()
    return args

def main(args):
    infile = args.input
    outfile = args.output
    in_encode = args.encoding

    outs = []

    with codecs.open(infile, 'r', encoding=in_encode) as f:
        for i,line in enumerate(f):
            print(line)
            out={}
            if i == 0:
                keys = line.strip().split(',')

            else:
                values = line.strip().split(',')
                for k,v in zip(keys,values):
                    if k == 'No':
                        out[k] = int(v)
                    else:
                        out[k] = v

                outs.append(out)


    with open(outfile, 'w', encoding='utf-8') as f:
        for out in outs:
            jout = json.dumps(out,ensure_ascii=False)
            print(jout, file=f)
        
if __name__ == '__main__':
    args = argument()
    main(args)
