#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import re
import codecs
import os
import sys
import glob
from os.path import basename
from src.sentence import aplign_pair

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
    output_file= output_dir + base_name + ".ss"
    # Empty file.
    open(output_file, 'w').close()
    content_buff=""
    line_count = 0
    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:

        for line in sourceFile.readlines():
            line_count = line_count + 1
            tokens=line.strip().split('\t')

            en_ss = tokens[0]
            th_ss = tokens[1].rstrip('.')

            # Clean tag a bit.
            en_ss = re.sub(r'{\\[a-zA-Z]+}', '', en_ss)
            th_ss = re.sub(r'{\\[a-zA-Z]+}', '', th_ss)
            en_ss = re.sub(r'<[a-zA-Z]+>', '', en_ss)
            th_ss = re.sub(r'<[a-zA-Z]+>', '', th_ss)
            en_ss = re.sub(r'<\/[a-zA-Z]+>', '', en_ss)
            th_ss = re.sub(r'<\/[a-zA-Z]+>', '', th_ss)

            print(str(line_count) + " #####################")

            # TODO, toggle forward/backward and increase error to get converge.
            aplign_pair(en_ss, th_ss, 5, True)









