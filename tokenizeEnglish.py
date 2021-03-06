#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import codecs
from os.path import basename
from nltk.tokenize import TweetTokenizer

encode_type="UTF-8"

dirname = sys.argv[-1]
dirname = dirname.strip()
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + '*.txt'
list_file=glob.glob(to_data_path)


# Tokenize.
word_tokenize = TweetTokenizer()
def tokenize_eng(text):
    tokens = word_tokenize.tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        content_buff = content_buff + " " + word
    content_buff = ' '.join(content_buff.split())
    content_buff = re.sub(r"([a-zA-Z0-9])(\')([a-zA-Z0-9])", r'\1 \2\3', content_buff)
    return( content_buff.strip() )

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

    # Tokenize.
    wordTokenize = TweetTokenizer()

    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        line_count=0
        prev_st=''
        for line in sourceFile.readlines():
            # content = clean_content(line, ' ')
            line=line.strip()
            line = ' '.join(line.split())
            if(line==""):
                content_buff += line
                content_buff += "\n"
                continue

            if (line==prev_st):
                content_tmp=prev_tok
            else:
                content_tmp = tokenize_eng(line)
                # content_tmp = re.sub(r"([a-zA-Z0-9])(\')([a-zA-Z0-9])", r'\1 \2\3', content_tmp)

            # print(content_tmp)
            content_buff = content_buff + content_tmp + "\n"
            prev_st = line
            prev_tok = content_tmp
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
