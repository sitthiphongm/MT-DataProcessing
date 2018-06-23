import nltk
import re
import codecs
import os
import sys
import glob
from os.path import basename
from nltk.tokenize import sent_tokenize
from nltk.tokenize import regexp_tokenize

encode_type="UTF-8"

dirname = sys.argv[-1]
dirname = dirname.strip()
# dirname=os.path.dirname(dirname)+"/"
if dirname[-1] != "/":
    dirname+="/"
# print(dirname)

to_data_path = dirname + '*.tab'
list_file=glob.glob(to_data_path)

pattern = r'''(?x)          # set flag to allow verbose regexps
        (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
      | \w+(?:-\w+)*        # words with optional internal hyphens
      | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
      | \.\.\.              # ellipsis
      | [][.,;"'?():_`-]    # these are separate tokens; includes ], [
    '''

for input_file in list_file:
    print(input_file)
    output_dir=os.path.dirname(input_file)+"/"
    base_name=str(basename(input_file)).split(".")
    base_name=base_name[0]
    output_file= output_dir + base_name + ".ss"
    # Empty file.
    open(output_file, 'w').close()
    content_buff=""
    line_count = 0
    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        line_count=0
        for line in sourceFile.readlines():
            tokens=line.strip().split('\t')

            en_ss = tokens[0]
            th_ss = tokens[1].rstrip('.')

            sent_en_list = sent_tokenize(en_ss)
            sent_th_list = th_ss.split()



            #####
            if (len(sent_en_list) == 1 or len(sent_th_list) == 1):
                pass
            elif (len(sent_en_list) == len(sent_th_list)):
                pass
            else:
                # Character ratio
                ratio=len(en_ss) / len(th_ss)

                print('\n:::::: ' + str(ratio))

                # join sentence
                # del a[-1]


                len_th=sent_th_list[:]
                for i in range(len(len_th)):
                    num_char = len(sent_th_list[i])
                    if (ratio > 1):
                        len_th[i] = num_char*ratio
                    else:
                        len_th[i] = num_char

                print(sent_th_list)
                print(len_th)



                len_en=sent_en_list[:]
                for i in range(len(len_en)):
                    num_char = len(sent_en_list[i])
                    if (ratio < 1):
                        len_en[i]=num_char*ratio
                    else:
                        len_en[i] = num_char

                print(sent_en_list)
                print(len_en)



