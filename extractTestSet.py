#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import re
import codecs
import os
import sys
import glob
from os.path import basename
from src.dictionary import *
from collections import OrderedDict

import numpy as np
import scipy.stats as stats
import pylab as pl


from nltk.tokenize import sent_tokenize as split_sentence_en
from src.sentence import split_sentence_th

encode_type="UTF-8"

DEFAULT_PERCENT_ERROR=5

dirname = sys.argv[-1]
dirname = dirname.strip()
# dirname=os.path.dirname(dirname)+"/"
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + '*.hun.txt'
list_file=glob.glob(to_data_path)


def eng_match(strg, search=re.compile(r'[^a-zA-Z0-9 .]').search):
    return not bool(search(strg))

def thai_match(strg, search=re.compile(r'[^ก-๛0-9 ]').search):
    return not bool(search(strg))

# print(special_match("az "))

# exit(0)


for input_file in list_file:
    print(input_file)
    output_dir=os.path.dirname(input_file)+"/"
    base_name=str(basename(input_file)).split(".")
    base_name=base_name[0]
    output_file= output_dir + base_name + ".TUTs.tab"
    content_buff=''

    # Empty file.
    open(output_file, 'w').close()

    content_buff=""
    line_count = 0

    hist={}

    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:

        for line in sourceFile.readlines():
            # line_count = line_count + 1
            tokens=line.strip().split('\t')

            if len(tokens)==3:
                source_s = tokens[0].lstrip('-').strip()
                target_s = tokens[1].rstrip('.').lstrip('-').strip()
                hun_score= float(tokens[2])

                st = (source_s + '\t' + target_s)

                hist[st]=hun_score

            else:
                # print(line_count, line.strip())
                line_count += 1
                continue

        hist_sorted = OrderedDict(sorted(hist.items(), key=lambda x: x[1], reverse=True))
        count_tuts=0
        content={}
        for st,value in hist_sorted.items():
            # print(value, key)
            target_st = st.split('\t')[1].strip()
            source_st = st.split('\t')[0].strip()

            len_source=len(source_st.split(" "))
            len_target=len(target_st.split(" "))

            source_words = source_st.split(" ")

            diff = 100 * (abs(len_source-len_target) / max(len_source, len_target))

            if (re.search(r'^[A-Z]', source_st)) and (len_source > 8) and (len_source < 20) and (diff < 30 ) and value>0.7:
                if (eng_match(source_st) and thai_match(target_st)):
                    content[source_words[0] + ' ' + source_words[1] + ' ' + source_words[2]] = st
                    count_tuts = count_tuts + 1
                    if len(content) == 3500:
                        break

        for value,st in content.items():
            print(value, st)
            content_buff = content_buff + st + '\n'

        file = codecs.open(output_file, "a", "utf-8")
        file.write(content_buff)
        file.close()
        content_buff = ""


