import re
import argparse
from pathlib import Path

non_japanese = re.compile('^[^一-龥ぁ-んァ-ヶ\n]+$')
sub_non_japanese = re.compile('[^一-龥ぁ-んァ-ヶ]*[(DOI)|(JSME)|(Mechanical)][^一-龥ぁ-んァ-ヶ\n]+')
paragraph = re.compile('^[1-9][.・] +')
paragraph_return = re.compile('[1-9][.・][1-9]*  +[一-龥ぁ-んァ-ヶ]')
reference = re.compile('^文 +?献$')
paragraph_patent = re.compile('【.+】')
patent_ref = re.compile('特[開表].*公報')
zu = re.compile('^[ 　]*?[図表][0-9０-９]+$')


def paper_proc(read, write):
    for line in read:
        if non_japanese.match(line):
            continue
        if paragraph.match(line):
            print("\n", file=write)
        
        new_line = paragraph_return.sub('\n\n\g<0>', line.strip())
        if reference.match(new_line):
            break
        new_line = sub_non_japanese.sub('', new_line)
        print(new_line, end='', file=write)

        
def patent_proc(read, write):
    for line in read:
        new_line = line.strip()
        if paragraph_patent.search(new_line):
            print('\n', file=write)
            new_line = paragraph_patent.sub('', new_line)
        if non_japanese.match(new_line) or zu.match(new_line):
            continue
        new_line = patent_ref.sub('', new_line)
            
        print(new_line, end='', file=write)
    

def main(args):
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    if not(output_dir.exists()):
        output_dir.mkdir(parents=True)

    mode = args.mode
    if mode == 'paper':
        proc = paper_proc
    elif mode == 'patent':
        proc = patent_proc

    input_files = input_dir.glob('*.txt')
    for input_file in input_files:
        output_file = output_dir.joinpath(str(input_file.stem) + '_post' + str(input_file.suffix))
        print(input_file)
        with input_file.open(mode='r') as f:
            with output_file.open(mode='w') as g:
                proc(f, g)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='exclude noisy sentence')
    parser.add_argument('-i', '--input', help='select input dirctory')
    parser.add_argument('-o', '--output', help='select output dirctory')
    parser.add_argument('--mode', default='paper', help='select preprocmode paper or patent')

    args = parser.parse_args()
    main(args)
