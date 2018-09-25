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

import numpy as np
import scipy.stats as stats
import pylab as pl

from src.cleantext import clean_text


from nltk.tokenize import sent_tokenize as split_sentence_en
from src.sentence import split_sentence_th

encode_type="UTF-8"

DEFAULT_PERCENT_ERROR=5
DEFAULT_MAX_REPEAT=1
DEFAULT_HUN_TRESHOLD=0.70

dirname = sys.argv[-1]
dirname = dirname.strip()
# dirname=os.path.dirname(dirname)+"/"
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + '*.hun.txt'
list_file=glob.glob(to_data_path)

def escape(html):
    return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def html_decode(s):
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

for input_file in list_file:
    print(input_file)
    output_dir=os.path.dirname(input_file)+"/"
    base_name=str(basename(input_file)).split(".")
    base_name=base_name[0]
    output_file= output_dir + base_name + ".tab"
    content_buff=''

    # Empty file.
    if (os.path.isfile(output_file)):
        print('File Exist : ' + output_file)
        continue
    else:
        print('Process Output File : ' + output_file)
        # open(output_file, 'w').close()

    # sys.exit(0)
    open(output_file, 'w').close()

    content_buff=""
    line_count = 0

    hist=[]

    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        thresh=DEFAULT_HUN_TRESHOLD
        for line in sourceFile.readlines():
            # line_count = line_count + 1
            tokens=line.strip().split('\t')

            if len(tokens)==3:
                source_s = tokens[0]
                target_s = tokens[1].rstrip('.')
                hun_score= float(tokens[2])
                hist.append(hun_score)
            else:
                # print(line_count, line.strip())
                line_count += 1
                continue

        mean=np.mean(hist)
        sd=np.std(hist)
        thresh=1.5-mean
        print('==>',mean, sd, thresh)

    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        line_count = 0
        repeat=0
        st=''
        prev_st=''
        for line in sourceFile.readlines():
            # print(line_count, line.strip())
            # line_count = line_count + 1
            tokens=line.strip().split('\t')

            if len(tokens)==3:
                source_s = tokens[0].lstrip('-').lstrip('#').strip()
                target_s = tokens[1].rstrip('.').lstrip('-').lstrip('#').strip()

                # need to be the same with english.
                source_s = clean_text(source_s, 'en')
                target_s = clean_text(target_s, 'th')

                target_s = re.sub(r"([a-zA-Z0-9])(\')([a-zA-Z0-9])", r'\1 \2\3', target_s)

                if (re.search(r'ธปท', target_s)):
                    source_s = re.sub(r'bot|BOT|Bot', 'Bank of Thailand', source_s)
                    target_s = re.sub(r'ธปท.|ธปท', 'ธนาคาร แห่ง ประเทศไทย', target_s)

                hun_score = 0
                if (source_s=='' or target_s==''):
                    hun_score = 0
                elif (re.search(r' no no ', source_s)):
                    hun_score = 0
                elif (re.search(r' no , no ', source_s)):
                    hun_score = 0
                elif (re.search(r' oh , oh ', source_s)):
                    hun_score = 0
                else:
                    len_source = len(source_s.split(' '))
                    len_target = len(target_s.split(' '))
                    norm = (len_source + len_target) / 2
                    diff_count = int((100 * abs(len_source - len_target)) / max(len_source, len_target))
                    per = diff_count
                    if (norm <= 6):
                        per = diff_count * norm * 0.1
                    if per < 50:
                        hun_score= float(tokens[2])
                        while (re.search(r'([0-9]+)[ ]?([,|.|:|-|/])[ ]([0-9]+)', source_s)):
                            source_s = re.sub(r'([0-9]+)[ ]?([,|.|:|-|/])[ ]([0-9]+)', r'\1\2\3', source_s)
                        while (re.search(r'([0-9]+)[ ]?([,|.|:|-|/])[ ]([0-9]+)', target_s)):
                            target_s = re.sub(r'([0-9]+)[ ]?([,|.|:|-|/])[ ]([0-9]+)', r'\1\2\3', target_s)

                        if (re.search(r'([a-zA-Z]{2,})[-]([a-zA-Z]{2,})', source_s)):
                            target_s=re.sub(r'([ก-๛a-zA-Z]{2,})[ ]?([-])[ ]?([ก-๛a-zA-Z]{2,})', r'\1\2\3', target_s)

            else:
                # print(line_count, line.strip())
                # line_count += 1
                continue

            if hun_score > thresh:
                st=(source_s + '\t' + target_s)
                # format number to help word embedding&stat.
                st = re.sub(r'([0-9]{4})([-\/\.])(1[012]|0?[1-9])([-\/\.])([12][0-9]|3[01]|0?[1-9])\b', '@date@', st)
                st = re.sub(r'([0-9]{4})([-\/\.])([12][0-9]|3[01]|0?[1-9])([-\/\.])(1[012]|0?[1-9])\b', '@date@', st)
                st = re.sub(r'([12][0-9]|3[01]|0?[1-9])([-\/\.])(1[012]|0?[1-9])([-\/\.])([0-9]{4})\b', '@date@', st)
                st = re.sub(r'(([0-9]{1,3})([,]?[0-9]{3}){0,})([\.][0-9]+)?\b', '@num@', st)
                # st = st + ' ==> ' + target_s
                if (st != prev_st):
                    content_buff = content_buff + escape(st) + '\n'
                    line_count += 1
                prev_st=st

            # Flush buffer.
            if (line_count % 10000 == 0):
                file = codecs.open(output_file, "a", "utf-8")
                file.write(content_buff)
                file.close()
                content_buff = ""

        # Write last chunk.
        file = codecs.open(output_file, "a", "utf-8")
        file.write(content_buff)
        file.close()
        content_buff = ""

