TARGET_DIR="/data/language/corpus/aozora/aozorabunko/cards/"
UNZIP_DIR="/data/language/corpus/aozora/txt/sjis/"
UTF_DIR="/data/language/corpus/aozora/txt/utf8/"

pwd
cd ${UNZIP_DIR}
pwd
ls ${TARGET_DIR}

for FILE in $( find ${TARGET_DIR} -type f -name *.zip ); do
    echo ${FILE}
    dirname=`dirname ${FILE}`
    writedir=`echo ${dirname} | cut -d/ -f8`
    if [ ! -e $writedir ]; then
	mkdir $writedir
    fi
    unzip -n -d ${writedir} ${FILE}
done

cd ${UTF_DIR}

for FILE in $( find ${UNZIP_DIR} -type f -name *.txt ); do
    echo ${FILE}
    filename=`basename ${FILE}`
    dirname=`dirname ${FILE}`
    outfile=`echo $filename | cut -d '.' -f 1`
    writedir=`echo ${dirname} | cut -d/ -f8`
    if [ ! -e $writedir ]; then
	mkdir $writedir
    fi    
    nkf -Luw ${FILE} >> ${UTF_DIR}/${writedir}/${outfile}.txt
done				     
