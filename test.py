#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
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

encode_type="UTF-8"
encoding_t="ISO-8859-1"
PERCENT_ERROR=10

input_file=sys.argv[-1]

content_buff=''

text1 = "On a $50,000 mortgage of 30 years at 8 percent, the monthly payment would be $366.88."
text2="สวัสดีครับ   ผมเรย์ คินเซลล่า เป็นเกียรติที่ได้พบคุณ 10, ๕๔ คะแนน มากมาย, มากๆ จริง ๆ ครับ ผมผมผมผมผ"

# print(split_sentence_th(text2))


test='multiple covers_SIG_NEWLINE_of{i1} Entertainment Weekly;{i}'
content = re.sub(r'{[a-zA-Z]{1}[0-9]{0,2}}', '', test)

print(content)





















'''
pattern = r'[ก-๛]+[\ ][0-9]+s'

text="น.ส.ขนิษตา หลงจิ อายุ 20 ปี น้องสาวของนายธีรศักดิ์ กล่าวว่า ทางครอบครัวแม้จะทำใจมาตลอดเพราะศาลชั้นต้น"
tokens = re.split(pattern, text)

print(text)
print(tokens)
'''

'''
with codecs.open(input_file, "r", encoding=encoding_t) as sourceFile:
    for line in sourceFile.readlines():
        print( line.decode("iso-8859-1") )
        break
'''

'''
with codecs.open(input_file, "r", encoding="ISO-8859-1") as sourceFile:
    for line in sourceFile.readlines():
        # print(line)
        content = clean_content(line, ' ')
        if language_not_th_en(content):
            continue

        if (content!=''):
            content_buff += content + '\n'

# print(content_buff)

file = codecs.open('tmp/debug.txt', "w", "utf-8")
file.write(content_buff)
file.close()
'''

