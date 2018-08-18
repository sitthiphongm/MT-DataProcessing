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

encode_type="UTF-8"
encoding_t="ISO-8859-1"
PERCENT_ERROR=10

input_file=sys.argv[-1]

content_buff=''

def tokenize_eng(text):
    tokens = word_tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        content_buff = content_buff + " " + word
    content_buff = ' '.join(content_buff.split())
    return( content_buff.strip() )

text="Your affection for this X@-@ Man(has ruined you), Emma ."
tok=tokenize_eng(text)
print(tok)

tknzr = TweetTokenizer()
tokenized_sent=tknzr.tokenize(text)
# tokenized_sent = StanfordTokenizer().tokenize(text)
print(tokenized_sent)


content_buff_temp="Your affection for this X@-@ Man(has ruined you), Emma ."
content_buff_temp=re.sub(r'[\s]@-@[\s]', '-',content_buff_temp)
content_buff_temp=re.sub(r'[\s]@-@', '-',content_buff_temp)
content_buff_temp=re.sub(r'@-@[\s]', '-',content_buff_temp)
print(content_buff_temp)

'''
dictionaryThai={}
data_path = os.path.dirname(os.path.realpath(__file__))
dictionary_file_th = data_path + "/dict/TH-utf8.txt"
with codecs.open(dictionary_file_th, "r", encoding=encode_type) as dictFile:
    for line in dictFile.readlines():
        dictionaryThai[line.strip()] = 0

text1="น.ส. ขนิษตา หลงจิ อายุ 20 ปี น้องสาว ของ นาย ธีรศักดิ์ กล่าว ว่า ทาง ครอบครัว แม้ จะ ทำ ใจ มา ตลอด เพราะ ศาล ขั้นต้น"
print('source :: ' + text1)
tokens = detok_thai(text1, dictionaryThai)
print(tokens)

text2="สวัสดี ครับ   ผม เรย์ คินเซลล่า เป็น เกียรติ ที่ ได้ พบ คุณ 10, ๕๔ คะแนน มาก มาย, มาก ๆ จริง ๆ ครับ"
print('source :: ' + text2)
tokens = detok_thai(text2, dictionaryThai)
print(tokens)
'''

'''
text1 = "On a $50,000 mortgage of 30 years at 8 percent, the monthly payment would be $366.88."
text2="สวัสดีครับ   ผมเรย์ คินเซลล่า เป็นเกียรติที่ได้พบคุณ 10, ๕๔ คะแนน มากมาย, มากๆ จริง ๆ ครับ ผมผมผมผมผ"

# print(split_sentence_th(text2))

test='multiple covers_SIG_NEWLINE_of{i1} Entertainment Weekly;{i}'
content = re.sub(r'{[a-zA-Z]{1}[0-9]{0,2}}', '', test)

print(content)
'''

'''
pattern = r'[ก-๛]+[\ ][0-9]+s'

textss="น.ส.ขนิษตา หลงจิ อายุ 20 ปี น้องสาวของนายธีรศักดิ์ กล่าวว่า ทางครอบครัวแม้จะทำใจมาตลอดเพราะศาลชั้นต้น"
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

'''  
if key not in pair_buffer.keys():
    break                                           
content_s = str(pair_buffer[key])
content = clean_content(line, 'th')
if ((content_s != '') and (content != '')):
    source_english = re.search('[a-zA-Z]', content_s)
    target_english = re.search('[a-zA-Z]', content)
    source_thai = re.search('[ก-ฮ]', content_s)
    target_thai = re.search('[ก-ฮ]', content)
    out_text = ''
    if (source_english and target_thai):
        out_text = content_s + '\t' + content
    elif (source_thai and target_english):
        out_text = content + '\t' + content_s + ''
    # Wrong pair.
    if (out_text != ''):
        out_text_buff += out_text + '\n'
'''