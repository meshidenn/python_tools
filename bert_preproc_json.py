import argparse
import glob
import json
import os
import re


def body_proc(body):
    p1 = re.compile('。\([^」|)|）|"]\)')
    p2 = re.compile('^。')
    body.strip(" ")
    body.lower()
    body = p1.sub('。\n\1/g', body)
    body = p2.sub('', body)
    return body


def out_all(body_list, folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    with open(folder_name + "/all.txt", 'w', encoding='utf-8') as g:
        for body in body_list:
            print(body, file=g)
            g.write("\n")


def foldername(i, outfolder):
    base = ord('A')
    m, n = divmod(i, 25)
    return outfolder + "/" + chr(base + m) + chr(base + n)


def main(args):
    infolder = args.infolder
    outfolder = args.outfolder
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    
    path = infolder + "/*.json"
    flist = glob.glob(path)
    n = 0
    i = 0
    threash = 100000
    body_list = []
    for fname in flist:
        with open(fname, 'r', encoding='utf-8') as f:
            for line in f:
                jline = json.loads(line)
                if "kiji" in jline.keys():
                    body = jline["kiji"]
                    body_list.append(body_proc(body))
                    i += 1

                if (i > threash):
                    folder_name = foldername(n, outfolder)
                    out_all(body_list, folder_name)
                    body_list = []
                    i = 0
                    n += 1

                    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infolder", help="designate input folder name")
    parser.add_argument("-o", "--outfolder", help="designate output folder name")
    args = parser.parse_args()
    main(args)
