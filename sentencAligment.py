#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import re
import codecs
import os
import sys
import glob
from os.path import basename
from nltk.tokenize import sent_tokenize as split_sentence_en
from src.sentence import split_sentence_th

encode_type="UTF-8"

DEFAULT_PERCENT_ERROR=5

dirname = sys.argv[-1]
dirname = dirname.strip()
# dirname=os.path.dirname(dirname)+"/"
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + '*.tab'
list_file=glob.glob(to_data_path)

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

            # Clean tag.
            en_ss = re.sub(r'{\\[a-zA-Z]+}', '', en_ss)
            th_ss = re.sub(r'{\\[a-zA-Z]+}', '', th_ss)
            en_ss = re.sub(r'<[a-zA-Z]+>', '', en_ss)
            th_ss = re.sub(r'<[a-zA-Z]+>', '', th_ss)
            en_ss = re.sub(r'<\/[a-zA-Z]+>', '', en_ss)
            th_ss = re.sub(r'<\/[a-zA-Z]+>', '', th_ss)

            sent_en_list = split_sentence_en(en_ss)
            sent_th_list = split_sentence_th(th_ss)


            #####
            if (len(sent_en_list) == 1 or len(sent_th_list) == 1):
                pass
            elif (len(sent_en_list) == len(sent_th_list)):
                pass
            else:
                # Character ratio
                ratio=len(en_ss) / len(th_ss)

                print('\n:::::: ' + str(ratio))

                # Join in Thai.
                # 1) Join ,;..... and space
                # 2)

                print(en_ss)
                print(th_ss)

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



