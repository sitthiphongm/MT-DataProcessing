#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import os
import sys
import glob
from langdetect import detect
from os.path import basename
from src.sentence import *

from src.language import language_mixed_en
from src.dictionary import *

import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))

encode_type="UTF-8"

dirname = sys.argv[-1]
dirname = dirname.strip()
if dirname[-1] != "/":
    dirname+="/"

to_data_path = dirname + '*.tok'
list_file=glob.glob(to_data_path)

# load dictionary
dictionary={}
dictionaryThai={}
dictionary=loadDictionary()
dictionaryThai=loadThaiDictionary()
# sys.exit(0)

countUnAlign=0
countNGram={}
for target_word, source_word in dictionary.items():
    count_source=len(source_word.split())
    count_target = len(target_word.split())
    if count_source!=count_target and count_target>count_source and count_source<=4:
        if source_word not in stopWords:
            countUnAlign = countUnAlign + 1
            if count_source in countNGram:
                countNGram[count_source] = countNGram[count_source] + 1
            else:
                countNGram[count_source] =  1

            diff=count_target-count_source
            # if diff==1 and count_source==1:
                # new_target=detok_thai(target_word, dictionaryThai)
            print(str(count_source) + '\t' + str(count_target) + '\t' + source_word + '\t' + target_word )

# print('Total Unalign Count = ' + str(countUnAlign) )
#
# for key,vale in countNGram.items():
#    print('Total ' + str(key) + ' Gram = ' + str(vale))


