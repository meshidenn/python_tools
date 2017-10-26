import sys
import xmltodict
from collections import OrderedDict

def yield_items(value, separator, prefix = ''):
    if isinstance(value, dict):
        for key, val in value.items():
            yield from yield_items(val, separator, prefix + separator + key)
    else:
        yield prefix, value

def dict_flatten(dic, separator):
    return OrderedDict(yield_items(dic, separator))

def main(argc, argv):
    for filename in argv[1:]:
        with open(filename) as file:
            dic = xmltodict.parse(file.read())
            flatten_dic = dict_flatten(dic, ".")
            print(json.dumps(flatten_dic))

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
