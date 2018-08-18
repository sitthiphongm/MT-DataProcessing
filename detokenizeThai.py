#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import os
import sys
import glob
from os.path import basename
from src.globalSetting import *
from src.dictionary import *
from src.sentence import *

dirname = sys.argv[-1]
dirname = dirname.strip()
if dirname[-1] != "/":
    dirname+="/"
# print(dirname)
to_data_path = dirname + '*TH.txt'
list_file=glob.glob(to_data_path)

# load dictionary
dictionaryThai={}
dictionaryThai=loadThaiDictionary()
# sys.exit(0)

for input_file in list_file:
    print(input_file)
    output_dir=os.path.dirname(input_file)+"/"
    base_name=str(basename(input_file)).split(".")
    base_name=base_name[0]
    output_file= output_dir + base_name + ".detok.txt"
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


            # line="I 'm up to my waist in hot snizz"
            # line="ขึ้น รถ ไป เลยไป"

            detok_sense=detok_thai(line, dictionaryThai)

            # exit(0)

            # RED dot/new line, replace with empty
            content_buff_temp=detok_sense.strip()
            content_buff_temp = re.sub(r'[\s]@-@[\s]', '-', content_buff_temp)
            content_buff_temp = re.sub(r'[\s]@-@', '-', content_buff_temp)
            content_buff_temp = re.sub(r'@-@[\s]', '-', content_buff_temp)
            content_buff_temp = re.sub(r'\s([\'!?\.,])', r'\1', content_buff_temp)

            ''' to cintunue
            content_buff_temp=re.sub(r'\s(["\'])', r'\1', content_buff_temp)
            content_buff_temp=re.sub(r'("|\')([\ ])', r'\1', content_buff_temp)
            content_buff_temp = re.sub(r'(")(")', r'\1 \2', content_buff_temp)
            content_buff_temp = re.sub(r'([a-zA-Z])([\ ])(\,|.)', r'\1\3', content_buff_temp)
            content_buff_temp=re.sub(r'\s([?.!"\'](?:\s|$))', r'\1', content_buff_temp)
            '''

            # debug.
            if (re.search(r'[a-z]', detok_sense)):
            # if 1:
                print("-->")
                print(line)
                print(content_buff_temp)

            # print(content_buff_temp)
            content_buff=content_buff + content_buff_temp + "\n"

            line_count += 1
            # Flush data.
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
