#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os
import codecs
import shutil
import nltk
from langdetect import detect
from src.cleantext import clean_content
from src.language import language_not_en
from src.language import language_not_th_en
from nltk.tokenize import regexp_tokenize
from nltk.tokenize import sent_tokenize
from src.sentence import split_sentence_th
from src.sentence import detok_thai
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer

encode_type="UTF-8"
encoding_t="ISO-8859-1"
PERCENT_ERROR=10

input_file=sys.argv[1]
output_file=sys.argv[2]

filelist={}
with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
    for line in sourceFile:
        tokens=line.strip().split('\t')
        # print(tokens[0], tokens[1])
        filelist[tokens[1]]=tokens[0]

open(output_file, 'w').close()

for filename,multiply in filelist.items():
    print(filename, multiply)
    with codecs.open(filename, "r", encoding=encode_type) as ppfile:
        line_count=0
        content_buff=''
        for line in ppfile:
            text=line.strip()
            for _ in range(int(multiply)):
                content_buff = content_buff + text + "\n"
                line_count += 1

            # Flush data.
            if (line_count>10000):
                file = codecs.open(output_file, "a", encode_type)
                file.write(content_buff)
                file.close()
                content_buff = ""
                line_count=0
        # Write last chunk.
        file = codecs.open(output_file, "a", encode_type)
        file.write(content_buff)
        file.close()
        content_buff = ""
