import sys


def main(args):
    input_file_name = args[1]
    output_file_name = args[2]
    prefix = "en_"

    with open(input_file_name,  'r') as f:
        line = next(f)
        out_line = prefix + line
        with open(output_file_name, 'w') as g:
            print(out_line, file=g)
            
        for line in f:
            out_line = prefix + line
            with open(output_file_name, 'a') as g:
                print(out_line, file=g)


if __name__ == "__main__":
    args = sys.argv
    main(args)
