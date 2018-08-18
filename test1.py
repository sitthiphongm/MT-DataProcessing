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
from src.tokenize import tokenize_thai

encode_type="UTF-8"
encoding_t="ISO-8859-1"
PERCENT_ERROR=10

text='10,000 มหาศาลร้ายแรง 10.00 มหาศาล '
# tokens_th = tokenize_thai(text)

text='ร้ายแรง 10 , 00 มหาศาลร้ายแรง 10 , 000 , 000 , 000 มหาศาล'

'''
while(re.search(r'([0-9]+)[ ]([,])[ ]([0-9]+)', text)):
    text = re.sub(r'([0-9]+)[ ]([,|.|:])[ ]([0-9]+)', r'\1\2\3', text)
print(text)
'''

text='ร้ายแรง 10.00 มหาศาลร้ายแรง 10000000,000.000 มหาศาล '
out = re.sub(r'([0-9]{1,3})([,]?[0-9]{3}){0,}([\.][0-9]+)', '@num@', text)
print(out)

text='เวลา 10:30 ดีดี'
out = re.sub(r'([0-9]{1,2})([:]?[0-9]{1,2})', '@time@', text)
print(out)


source_s='list of governors of the BOT'
target_s= 'รายชื่อผู้ว่าการของ ธปท. ธปท'
if (re.search(r'ธปท.', target_s)):
    source_s = re.sub(r'bot|BOT|Bot', 'Bank of Thailand', source_s)
    target_s = re.sub(r'ธปท.|ธปท', 'ธนาคารแห่งประเทศไทย', target_s)

print(source_s,target_s)


'''
GENERAL	Num	^[ ]{0,3}[0-9]{1,3}[\.|\)][ ]		GENERAL13
GENERAL	Num	(?<=^|[ \"\'\t\(\-\+\,\≥\≤\/\[\:\\][ ]{0,5})(?<num>([\-|\+]?[0-9]{1,3})([,][0-9]{3}){0,})([\.][0-9]+)[a-z]\b		GENERAL14
GENERAL	Num	(?<=^|[ \"\'\t\(\-\+\,\≥\≤\/\[\:\\][ ]{0,5})(?<num>([\-|\+]?[0-9]{1,3})([,][0-9]{3}){0,})([\.][0-9]+)([\.][0-9]+)(?!\.)\b		GENERAL15
GENERAL	Num	(?<=^|[ \"\'\t\(\-\+\,\≥\≤\/\[\:\\][ ]{0,5})(?<num>([\-|\+]?[0-9]{1,3})([,]?[0-9]{3}){0,})([\.][0-9]+)?\b		GENERAL16
'''