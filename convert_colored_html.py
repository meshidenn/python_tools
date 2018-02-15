# -*- coding: utf-8 -*-

import json
import glob
import re
import os
import numpy as np


def topic_reader(infile):
    with open(infile, 'r', encoding='utf-8') as f:
        raw_wsk = json.load(f)

    wsk = raw_wsk['doc']
    return wsk


def content_reader(infile):
    lines = ''
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            lines += line

    return lines


def color_bar(i, topic):
    """
    make color bar depend on light spectral
    point1 = 0 : #ff0000 -> #ffff00
    point1 = 1 : #ffff00 -> #00ff00
    point1 = 2 : #00ff00 -> #00ffff
    point1 = 3 : #00ffff -> #0000ff
    point1 = 4 : #0000ff -> #ff00ff
    point1 = 5 : #ff00ff -> #ff0000

    index has length of each manipulation
    """
    n = 6
    q, mod = divmod(topic, n)
    index = []
    for _ in range(n):
        if mod > 0:
            index.append(q + 1)
            mod -= 1
        else:
            index.append(q)

    if topic != np.sum(index):
        print('unmach index topic:{}, sum_index:{}'.format(topic,
                                                           np.sum(index)))
        raise Exception

    tmp = 0
    for k, ind in enumerate(index):
        tmp += ind
        if i < tmp:
            point1 = k
            point2 = i - tmp
            break

    if point1 == 0:
        color_num = np.linspace(0, 255, index[0], dtype=int)[point2]
        if color_num < 16:
            x = str(format(color_num, 'x')) * 2
        else:
            x = str(format(color_num, 'x'))
        color = '#ff' + x + '00'
        return color
    elif point1 == 1:
        color_num = np.linspace(255, 0, index[1], dtype=int)[point2]
        if color_num < 16:
            x = str(format(color_num, 'x')) * 2
        else:
            x = str(format(color_num, 'x'))
        color = '#' + x + 'ff00'
        return color
    elif point1 == 2:
        color_num = np.linspace(0, 255, index[2], dtype=int)[point2]
        if color_num < 16:
            x = str(format(color_num, 'x')) * 2
        else:
            x = str(format(color_num, 'x'))
        color = '#00ff' + x
        return color
    elif point1 == 3:
        color_num = np.linspace(255, 0, index[3], dtype=int)[point2]
        if color_num < 16:
            x = str(format(color_num, 'x')) * 2
        else:
            x = str(format(color_num, 'x'))
        color = '#00' + x  + 'ff'
        return color
    elif point1 == 4:
        color_num = np.linspace(0, 255, index[4], dtype=int)[point2]
        if color_num < 16:
            x = str(format(color_num, 'x')) * 2
        else:
            x = str(format(color_num, 'x'))
        color = '#' + x + '00ff'
        return color
    elif point1 == 5:
        color_num = np.linspace(255, 0, index[5], dtype=int)[point2]
        if color_num < 16:
            x = str(format(color_num, 'x')) * 2
        else:
            x = str(format(color_num, 'x'))
        color = '#ff00' + x
        return color


def converter(wsks, lines, topic):
    for wsk in wsks:
        w, ts = list(wsk.items())[0]
        t = ts[1]
        c = color_bar(t, topic)
        cand = '(?<!\>)' + w + '(?![\<\/span\>][pancolorff])'
        rep = '<font color = ' + c + '>' + w + '</font>'
        try:
            lines = re.sub(cand, rep, lines, count=1)
        except re.error:
            print('pass:{}'.format(w))

    lines = '<html>\n <body>\n  <p>\n' + lines
    lines += '  </p>\n </body>\n</html>'
    return lines


def output(outfile, lines):
    with open(outfile, 'w', encoding='utf-8') as f:
        print(lines, file=f)


def main(args):
    jindir = args.jsoninput
    tindir = args.txtinput
    outdir = args.output
    topic = args.topic
    jinfiles = sorted(glob.glob(jindir + '/*.json'))
    tinfiles = sorted(glob.glob(tindir + '/*.txt'))
    print(jinfiles)
    print(tinfiles)

    try:
        os.mkdir(outdir)
    except FileExistsError:
        pass

    for jinfile, tinfile in zip(jinfiles, tinfiles):
        wsks = topic_reader(jinfile)
        lines = content_reader(tinfile)
        conv_lines = converter(wsks, lines, topic)
        outfile_name = '/' + tinfile.split('/')[-1].split('.txt')[0] + '.html'
        outfile = outdir + outfile_name
        output(outfile, conv_lines)

    outfile = outdir + 'colormap.html'
    with open(outfile, 'w', encoding='utf-8') as f:
        head = '<html>\n <body>\n  <p>\n'
        print(head, file=f)
        for i in range(topic):
            color = color_bar(i, topic)
            rep = '<font color = ' + color + '>あ</font>'
            print('{}:{}'.format(i, rep), file=f)

        tail = '  </p>\n </body>\n</html>'
        print(tail, file=f)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='decide input folder and output folder')
    parser.add_argument('--jsoninput', '-ji', dest='jsoninput', help='json input folder')
    parser.add_argument('--txtinput', '-ti', dest='txtinput', help='txt input folder')
    parser.add_argument('--topics', '-t', dest='topic', type=int, help='topic number')
    parser.add_argument('--output', '-o', dest='output', help='output folder')

    args = parser.parse_args()
    main(args)


