#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import os
import sys
import glob
# from langdetect import detect
from src.CleanText import clean_content
from src.language import language_not_en
from src.language import language_not_th_en
from os.path import basename

encode_type="UTF-8"

dirname = sys.argv[-1]
dirname = dirname.strip()
# dirname=os.path.dirname(dirname)+"/"
if dirname[-1] != "/":
    dirname+="/"
# print(dirname)

to_data_path = dirname + '*.txt'
list_file=glob.glob(to_data_path)

for input_file in list_file:
    print(input_file)
    output_dir=os.path.dirname(input_file)+"/"
    base_name=str(basename(input_file)).split(".")
    base_name=base_name[0]
    output_file= output_dir + base_name + ".detok"
    content_buff=''

    # Empty file.
    open(output_file, 'w').close()

    content_buff=""

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
             # RED dot/new line, replace with empty
            content_buff_temp=line.strip()
            content_buff_temp=re.sub(r"[\ ]@-@[\ ]|[\ ]@-@|@-@[\ ]", "-", content_buff_temp)
            content_buff_temp = re.sub(r'\s([\'!?\.,])', r'\1', content_buff_temp)
            # content_buff_temp = re.sub(r'\s([\"])', r'\1', content_buff_temp)

            # print(content_buff_temp)
            content_buff=content_buff + content_buff_temp + "\n"

            line_count += 1
            if (line_count%10000 == 0):
                file = codecs.open(output_file, "a", "utf-8")
                file.write(content_buff)
                file.close()
                content_buff=""
                # print(line_count)

    # Write last chunk.
    file = codecs.open(output_file, "a", "utf-8")
    file.write(content_buff)
    file.close()
    content_buff=""
