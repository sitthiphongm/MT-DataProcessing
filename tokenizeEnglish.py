#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import nltk
import codecs
from langdetect import detect
from src.CleanText import clean_content
from src.language import language_not_en
from src.language import language_not_th_en
from nltk.tokenize import word_tokenize
from pythainlp.tokenize import word_tokenize as word_tokenize_th
from os.path import basename

encode_type="UTF-8"

################### to move to .src #####################
def tokenize_eng(text):
    tokens = word_tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        content_buff = content_buff + " " + word
    content_buff = ' '.join(content_buff.split())
    return( content_buff.strip() )
#########################################################

dirname = sys.argv[-1]
dirname = dirname.strip()
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + '*.txt'
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
            content_buff = content_buff + tokenize_eng(line) + "\n"
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
