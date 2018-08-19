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
from src.language import language_not_enth
from nltk.tokenize import regexp_tokenize
from nltk.tokenize import sent_tokenize
from src.sentence import split_sentence_th
from src.sentence import detok_thai
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
# from src.tokenize import tokenize_thai

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

text='For other frequencies , scaling by the ratio of the frequencies ( for example , 1.5 Ghz = 1.65 Ghz / 1.5 Ghz × cycles per operation ) is sufficiently accurate to produce a reasonable sizing'
# text='list of governors of the BOT'
print(language_not_en(text))

text= 'รายชื่อผู้ว่าการของ ธปท. ธปท'
print(language_not_enth(text))

t1='aaa-bbb nnn - hhh'
t2='กก- bb '
t3='กก -bb'
t4='กก - bb'

while (re.search(r'([a-zA-Z]{2,})[-]([a-zA-Z]{2,})', t1)):
    print('YES')
    print(re.sub(r'([ก-๛a-zA-Z]{2,})[ ]?([-])[ ]?([ก-๛a-zA-Z]{2,})', r'\1\2\3', t1))
    print(re.sub(r'([ก-๛a-zA-Z]{2,})[ ]?([-])[ ]?([ก-๛a-zA-Z]{2,})', r'\1\2\3', t2))
    print(re.sub(r'([ก-๛a-zA-Z]{2,})[ ]?([-])[ ]?([ก-๛a-zA-Z]{2,})', r'\1\2\3', t3))
    print(re.sub(r'([ก-๛a-zA-Z]{2,})[ ]?([-])[ ]?([ก-๛a-zA-Z]{2,})', r'\1\2\3', t4))


print(source_s)


