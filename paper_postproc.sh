#/bin/bash

python paper_postproc.py -i /data/language/customer/solize/txt/JSME_papersA2011-2013/ -o /data/language/customer/solize/txt/post/JSME_papersA2011-2013/ --mode paper
python paper_postproc.py -i /data/language/customer/solize/txt/JSME_papersB2011-2013/ -o /data/language/customer/solize/txt/post/JSME_papersB2011-2013/ --mode paper
python paper_postproc.py -i /data/language/customer/solize/txt/JSME_papersC2011-2013/ -o /data/language/customer/solize/txt/post/JSME_papersC2011-2013/ --mode paper
# python paper_postproc.py -i /data/language/customer/solize/txt/JSME_papers2014-2018/ -o /data/language/customer/solize/txt/post/JSME_papers2014-2018/ --mode paper
# python paper_postproc.py -i /data/language/customer/solize/txt/01_fuelbattery/ -o /data/language/customer/solize/txt/post/01_fuelbattery/ --mode patent
# python paper_postproc.py -i /data/language/customer/solize/txt/02_battery/ -o /data/language/customer/solize/txt/post/02_battery/ --mode patent
# python paper_postproc.py -i /data/language/customer/solize/txt/03_highpressuretank/ -o /data/language/customer/solize/txt/post/03_highpressuretank/ --mode patent
