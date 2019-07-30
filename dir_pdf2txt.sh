#!/bin/bash

root="/data/language/customer/solize/txtq/"
suffix=".txt"
IFS=$'\n'
for filepath in `\find /data/language/customer/solize/ -type f -name *pdf`; do
    echo $filepath
    filename=`basename $filepath`
    dir=`dirname $filepath`
    writedir=$root`basename $dir`
    if [ ! -e $writedir ]; then
	mkdir $writedir
    fi
    outfile=`echo $filename | cut -d '.' -f 1`
    output=$writedir"/"$outfile$suffix
    python $HOME/work/pdfminer.six/tools/pdf2txt.py -o $output $filepath
    if [ $? -gt 0 ]; then
	echo "store file name in error.txt"
	echo $output >> $root"/error.txt"
    fi
    echo $output
done
