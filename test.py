import re
import sys
import codecs
import shutil
import nltk
from langdetect import detect
from src.CleanText import clean_content
from src.language import language_not_en
from src.language import language_not_th_en
from nltk.tokenize import regexp_tokenize

encode_type="UTF-8"
encoding_t="ISO-8859-1"

input_file=sys.argv[-1]

content_buff=''


pattern = r'[ก-๛]+[\ ][0-9]+s'

text="น.ส.ขนิษตา หลงจิ อายุ 20 ปี น้องสาวของนายธีรศักดิ์ กล่าวว่า ทางครอบครัวแม้จะทำใจมาตลอดเพราะศาลชั้นต้น"
tokens = re.split(pattern, text)

print(text)
print(tokens)

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

