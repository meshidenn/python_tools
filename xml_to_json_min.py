# -*- coding:utf-8 -*-

import xmltodict
import sys
import json
from collections import OrderedDict

def main(infile, outfile):
    raw_xml = ''
    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            raw_xml += line

    dict_xml = xml2dict(raw_xml)

    tree = ['SPTVML', 'SIInformations', 'SIInformation']
    keys = ['@contentsId', '@programId', 'ChannelGenre', 'ChannelName', 'Title', 'ShortTitle', 'Synopsis', 'DAMSynopsis']
    json_mins = ex_ns(dict_xml, tree, keys)

    with open(outfile, 'w', encoding='utf-8') as g:
        for json_min in json_mins:
            json_xml = dict2json(json_min)
            print(json_xml,file=g)

def xml2dict(raw_str):
    dict_xml = xmltodict.parse(raw_str)
    return dict_xml

def dict2json(dict_obj):
    json_xml = json.dumps(dict_obj)
    return json_xml

def ex_ns(json_obj,tree,ns_keys):
    json_mins = []
    tmp = json_obj
    for t in tree:
        if type(t) != 'list':
            tmp = tmp[t]
        else:
            for tm in tmp:
                if tm.key == t:
                    tmp = tmp[t]

    for t in tmp:
        json_min = OrderedDict()
        for key in ns_keys:
            if key in t.keys():
                json_min[key.strip('@')] = t[key]
            else:
                json_min[key.strip('@')] = ''

        if not(json_min['contentsId'] == ''):
            json_mins.append(json_min)

    return json_mins
    

if __name__ == '__main__':
    '''
    format exxample
    $python xml_to_json_min.py infile outfile
    '''
    
    infile = sys.argv[1]
    outfile = sys.argv[2]

    main(infile, outfile)
