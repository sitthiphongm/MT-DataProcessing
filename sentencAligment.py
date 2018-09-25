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

from nltk.tokenize import sent_tokenize as split_sentence_en
from src.sentence import split_sentence_th

encode_type="UTF-8"

DEFAULT_PERCENT_ERROR=5

dirname = sys.argv[-1]
dirname = dirname.strip()
# dirname=os.path.dirname(dirname)+"/"
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + 'it/en/*.tok'
list_file=glob.glob(to_data_path)

# create if not exist.
# createHunDictionary()
# split file.
# os.system('hunalign/hunalign -text -utf dict/th-en.hun.dic hunalign/example/Titles.EN hunalign/example/Titles.TH > hunalign/example/Titles.HUN.txt')

os.system('rm -rf data/temp/source/*')
os.system('rm -rf data/temp/target/*')
# os.system('rm -rf data/temp/output/*')
os.system('mkdir -p data/temp/source')
os.system('mkdir -p data/temp/target')
os.system('mkdir -p data/temp/output')

for input_file in list_file:
    print(input_file)
    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        output_dir = os.path.dirname(input_file) + "/"
        base_name = str(basename(input_file)).split(".")
        file_name = str(basename(input_file))
        base_name = base_name[0]

        file_count=0
        line_count=0
        content_buff = ""
        for line in sourceFile.readlines():
            content_buff = content_buff + line.strip() + "\n"
            line_count += 1
            if (line_count%10000 == 0):
                output_file='data/temp/source/' + str(file_count) + '.txt'
                file = codecs.open(output_file, "a", "utf-8")
                file.write(content_buff)
                file.close()
                content_buff=""
                file_count=file_count+1
        # Write last chunk.
        output_file = 'data/temp/source/' + str(file_count) + '.txt'
        file = codecs.open(output_file, "a", "utf-8")
        file.write(content_buff)
        file.close()
        content_buff=""
        file_count=file_count+1

    input_file=input_file.replace('it/en', 'it/th')
    print(input_file)

    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        output_dir = os.path.dirname(input_file) + "/"
        base_name = str(basename(input_file)).split(".")
        file_name = str(basename(input_file))
        base_name = base_name[0]
        file_count=0
        line_count=0
        content_buff = ""
        for line in sourceFile.readlines():
            content_buff = content_buff + line.strip() + "\n"
            line_count += 1
            if (line_count%10000 == 0):
                output_file = 'data/temp/target/' + str(file_count) + '.txt'
                file = codecs.open(output_file, "a", "utf-8")
                file.write(content_buff)
                file.close()
                content_buff=""
                file_count=file_count+1
        # Write last chunk.
        output_file = 'data/temp/target/' + str(file_count) + '.txt'
        file = codecs.open(output_file, "a", "utf-8")
        file.write(content_buff)
        file.close()
        content_buff=""
        file_count=file_count+1

    to_temp_path = dirname + 'temp/source/*'
    list_temp_file = glob.glob(to_temp_path)
    for temp_file in list_temp_file:
        source_file=temp_file
        target_file=temp_file.replace('/source/', '/target/')
        output_file=temp_file.replace('/source/', '/output/')
        # print(source_file, target_file, output_file)
        command_line='hunalign/hunalign -text -utf dict/th-en.hun.dic' + ' ' + source_file + ' ' + target_file + ' > ' + output_file
        print(command_line)
        os.system(command_line)

    file_merged = 'data/temp/output/' + base_name + ".hun.txt"
    # Empty file.
    open(file_merged, 'w').close()
    for i in range(file_count):
        file_to_merge  = 'data/temp/output/' + str(i) + '.txt'
        # print(file_to_merge, file_merged)
        command_line = 'cat ' + file_to_merge + ' >> ' + file_merged
        os.system(command_line)
        command_line = 'rm -rf ' + file_to_merge
        os.system(command_line)

    os.system('rm -rf data/temp/source/*')
    os.system('rm -rf data/temp/target/*')

