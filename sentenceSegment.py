#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import re
import codecs
import os
import sys
import glob
from os.path import basename
from src.sentence import *

encode_type="UTF-8"

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

    output_file_ss= output_dir + base_name + ".SS"
    output_file_noss = output_dir + base_name + ".NoSS"

    # Empty file.
    open(output_file_ss, 'w').close()
    open(output_file_noss, 'w').close()

    content_buff_ss=""
    content_buff_noss = ""
    line_count = 0
    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:

        for line in sourceFile.readlines():
            # line_count = line_count + 1
            tokens=line.strip().split('\t')

            if len(tokens)==2:
                source_s = tokens[0]
                target_s = tokens[1].rstrip('.')
            else:
                print(line_count, line.strip())
                line_count += 1
                continue

            # clean tag a bit.
            source_s = re.sub(r'{\\[a-zA-Z]+}', '', source_s)
            target_s = re.sub(r'{\\[a-zA-Z]+}', '', target_s)
            source_s = re.sub(r'<[a-zA-Z]+>', '', source_s)
            target_s = re.sub(r'<[a-zA-Z]+>', '', target_s)
            source_s = re.sub(r'<\/[a-zA-Z]+>', '', source_s)
            target_s = re.sub(r'<\/[a-zA-Z]+>', '', target_s)

            # TODO, toggle forward/backward and increase error to get converge.
            # for percentErrr in range(5,20):
            #    aplign_pair(source_s, target_s, percentErrr, True)

            sourceSentence = split_sentence_en(source_s)
            targetSentence = split_sentence_th(target_s)

            source_len=len(sourceSentence)
            target_len=len(targetSentence)
            if source_len<target_len:
                num_sentence=source_len
            else:
                num_sentence=target_len

            if (source_len== 1 or target_len == 1):
                # print('\n')
                # print(str(line_count) + "==> ", line.strip())
                source_s=source_s.replace("__JOINT__","")
                target_s=target_s.replace("__JOINT__", "")
                temp_st=source_s + '\t' + target_s
                if temp_st.find("_SIG_JOINLINE_")==-1:
                    content_buff_noss = content_buff_noss + temp_st + '\n'
            else:
                # print('\n')
                # print(str(line_count) + "==> ", line.strip())
                for st in range(0,num_sentence):
                    content_buff_ss = content_buff_ss + (sourceSentence[st] + '\t' + targetSentence[st]) + '\n'

            line_count += 1
            if (line_count%10000 == 0):
                file = codecs.open(output_file_ss, "a", "utf-8")
                file.write(content_buff_ss)
                file.close()
                content_buff_ss=""

                file = codecs.open(output_file_noss, "a", "utf-8")
                file.write(content_buff_noss)
                file.close()
                content_buff_noss=""

        # Write last chunk.
        file = codecs.open(output_file_ss, "a", "utf-8")
        file.write(content_buff_ss)
        file.close()
        content_buff_ss=""

        file = codecs.open(output_file_noss, "a", "utf-8")
        file.write(content_buff_noss)
        file.close()
        content_buff_noss=""





