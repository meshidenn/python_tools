import json
import sys
import codecs

def main(args):
    infile = args[1]
    outfile = args[2]

    outs = []

    with codecs.open(infile, 'r', encoding='utf_8_sig') as f:
        for i,line in enumerate(f):
            print(line)
            out={}
            if i == 0:
                keys = line.strip().split(',')

            else:
                values = line.strip().split(',')
                for k,v in zip(keys,values):
                    out[k] = v

                outs.append(out)


    with open(outfile, 'w', encoding='utf-8') as f:
        for out in outs:
            jout = json.dumps(out,ensure_ascii=False)
            print(jout, file=f)
        
if __name__ == '__main__':
    args = sys.argv
    main(args)
