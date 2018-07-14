#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import os
import sys
import glob
from langdetect import detect
from os.path import basename
import deepcut
from src.language import language_mixed_en
from src.language import language_mixed_th
from src.tokenize import tokenize_thai
from src.tokenize import tokenize_eng

encode_type="UTF-8"

dirname = sys.argv[-1]
dirname = dirname.strip()
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + '*detok.TH.txt'
list_file=glob.glob(to_data_path)

for input_file in list_file:
    print(input_file)
    output_dir=os.path.dirname(input_file)+"/"
    base_name=str(basename(input_file)).split(".")
    base_name=base_name[0]
    output_file= output_dir + base_name + ".tok"
    # Empty file.
    open(output_file, 'w').close()
    content_buff=""
    line_count = 0
    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        line_count=0
        for line in sourceFile.readlines():
            # content = clean_content(line, ' ')
            line=line.strip()
            line = ' '.join(line.split())
            if(line==""):
                content_buff += line
                content_buff += "\n"
                continue

            content_buff_temp = ""
            if language_mixed_en(line):
                word_list = active_content = line.split(" ")
                text_tmp = "";
                tokens_eng = ""
                tokens_th = ""
                for word in word_list:
                    # print(word)
                    try:
                        lang = detect(word)
                    except:
                        lang = "en"

                    if lang == "th":
                        # tokenize_thai(text):
                        # print(word + " : " + detect(word))
                        tokens_eng = tokenize_eng(text_tmp)
                        tokens_th = tokenize_thai(word)
                        content_buff_temp = content_buff_temp + " " + tokens_eng + " " + tokens_th
                        tokens_eng = ""
                        tokens_th = ""
                        text_tmp = ""
                    else:
                        text_tmp = text_tmp + " " + word
                if text_tmp != "":
                    tokens_eng = tokenize_eng(text_tmp)
                    content_buff_temp = content_buff_temp + " " + tokens_eng
            else:
                content_buff_temp = tokenize_thai(line)
            content_buff = content_buff + content_buff_temp.strip() + "\n"
            line_count += 1
            # Flush data.
            if (line_count%10000 == 0):
                file = codecs.open(output_file, "a", encode_type)
                file.write(content_buff)
                file.close()
                content_buff=""

        # Write last chunk.
        file = codecs.open(output_file, "a", encode_type)
        file.write(content_buff)
        file.close()
        content_buff=""








