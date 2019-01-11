import json
import codecs
import argparse
import csv


def argument():
    parser = argparse.ArgumentParser(description='convert csv to jsonl')
    parser.add_argument('--input', '-i')
    parser.add_argument('--output', '-o')
    parser.add_argument('--encoding', '-e', default='utf-8')

    args = parser.parse_args()
    return args


def main(args):
    infile = args.input
    outfile = args.output
    in_encode = args.encoding

    outs = []
    errors = []

    with codecs.open(infile, 'r', encoding=in_encode) as f:
        reader = csv.reader(f)
        try:
            for i, line in enumerate(reader):
                print(line)
                out = {}
                if i == 0:
                    keys = line

                else:
                    values = line
                    for k, v in zip(keys, values):
                        out[k] = v

                    outs.append(out)
        except:
            errors.append(i)

    with open(outfile, 'w', encoding='utf-8') as f:
        for out in outs:
            jout = json.dumps(out, ensure_ascii=False)
            print(jout, file=f)

    with open("col.err", 'w', encoding='utf-8') as f:
        print(errors, file=f)


if __name__ == '__main__':
    args = argument()
    main(args)
