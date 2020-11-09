import re
import argparse
from pathlib import Path

# check wheathre the line is a non japanese line
non_japanese = re.compile('^[^一-龥ぁ-んァ-ヶ\n]+$')

# pattern to remove non japanese part in a line
sub_non_japanese = re.compile('[^一-龥ぁ-んァ-ヶ]*[(DOI)|(JSME)|(Mechanical)][^一-龥ぁ-んァ-ヶ\n]+')

# check if the line is a paragraph title or not 
paragraph = re.compile('^[1-9][.・] +')

# pattern to remove structure info for patagraph title
paragraph_return = re.compile('[1-9][.・][1-9]*  +[一-龥ぁ-んァ-ヶ]')

# check if the line is start of reference
reference = re.compile('^文 +?献$')

# check wheather paragraph title is or not
paragraph_patent = re.compile('【.+】')

# pattarn to remove in a patent
patent_ref = re.compile('特[開表].*公報')

# table or figure caption line
zu = re.compile('^[ 　]*?[図表][0-9０-９]+$')


def paper_proc(read, write):
    for line in read:
        if non_japanese.match(line):
            # skip a non japanese line
            continue
        if paragraph.match(line):
            # insert null line between paragraph
            print("\n", file=write)

        # remove title specific info
        new_line = paragraph_return.sub('\n\n\g<0>', line.strip())
    
        if reference.match(new_line):
            # stop reading a file at a refenrece line
            break

        # remove non japanese part
        new_line = sub_non_japanese.sub('', new_line)
        print(new_line, end='', file=write)

        
def patent_proc(read, write):
    for line in read:
        new_line = line.strip()
        if paragraph_patent.search(new_line):
            # insert null line between paragraph
            print('\n', file=write)
            new_line = paragraph_patent.sub('', new_line)
            
        if non_japanese.match(new_line) or zu.match(new_line):
            # skip non_japanese line or table or figure caption line
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
