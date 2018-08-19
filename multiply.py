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

encode_type="UTF-8"
encoding_t="ISO-8859-1"
PERCENT_ERROR=10

input_file=sys.argv[1]
output_file=sys.argv[2]

# remove for now.
try:
    if (sys.argv[3])=='True':
        print('Convert to Lowercase..')
        lowercase=True
    else:
        lowercase=False
except:
    lowercase=False

filelist={}
with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
    for line in sourceFile:
        tokens=line.strip().split('\t')
        # print(tokens[0], tokens[1])
        filelist[tokens[1]]=tokens[0]

print('Clear Output File..')
open(output_file, 'w').close()

for filename,multiply in filelist.items():
    print(filename, multiply)
    multiply=int(multiply)
    with codecs.open(filename, "r", encoding=encode_type) as ppfile:
        line_count=0
        content_buff=''
        for line in ppfile:
            text=line.strip()
            for i in range(int(multiply)):
                # lower case for the last one.
                if ((i==(multiply-1)) and (multiply > 2)):
                    text = text.lower()
                content_buff = content_buff + text + "\n"
                line_count += 1

            # Flush data.
            if (line_count>50000):
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
