#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import glob
import codecs
from langdetect import detect
from src.CleanText import find_between_r
from src.CleanText import find_between

BLOCKSIZE = 1048576
encode_type_en="UTF-8"
encode_type_th="TIS-620"
encode_type=['TIS-620','UTF-8','LATIN-1','ISO-8859-1','ISO-8859-7', 'ISO-8859-5','ISO-8859-8']

curr_path = os.path.dirname(os.path.realpath(__file__))
data_path = curr_path + '/data/original/*'
en_files = glob.glob(data_path)

file_number=0
for source_file in en_files:
    out_text_buff=''

    # file name.
    use_name = source_file.split('\\')
    use_name = use_name[-1]
    split_use_name = use_name.split('.')
    # print(use_name)
    use_name = split_use_name[0]
    ext_name = split_use_name[2]


    file_number=file_number+1
    print('progress : ' + str(file_number))

    # skip if already convert.
    t_name = curr_path + '\\data\\unicode\\' + use_name + '.' + ext_name
    try:
        file_exist = open(t_name, "r")
        file_exist.close()
        continue
    except FileNotFoundError:
        pass

    # output text.
    out_text_buff=''
    content_buff=''

    # try many encoding type. not all files encoding the same.
    for encoding_t in encode_type:
        try:
            with codecs.open(source_file, "r", encoding=encoding_t) as decodeFile:
                loop=0
                for line in decodeFile.readlines():
                    out_text_buff += line
                    content = ((find_between_r(line, ',,', '\n'))).replace('\\N', '')
                    content = content.lstrip('-')
                    content = content.strip()
                    content_buff += content

                # what is the language in content?
                try:
                    lang = detect(content_buff)
                except:
                    lang = 'none'

                if (lang!='en' and lang!='th'):
                    print(' ' + lang)
                    print(content_buff)
                    # formatting encoding type to utf-8.
                    target_file = curr_path + '\\data\\decode-error\\' + use_name + '.' + ext_name

                    '''
                    print(encoding_t + ' : ' + use_name)
                    file = codecs.open(use_name, "w")
                    file.write(out_text_buff)
                    file.close()  # print()
                    '''

                    with open(source_file, "r") as sourceFile:
                        with codecs.open(target_file, "w") as targetFile:
                            while True:
                                contents = sourceFile.read(BLOCKSIZE)
                                if not contents:
                                    break
                                targetFile.write(contents)
                    continue

                # formatting encoding type to utf-8.
                use_name = curr_path + '\\data\\unicode\\' + use_name + '.' + lang
                print(encoding_t + ' : ' + use_name)
                file = codecs.open(use_name, "w", "utf-8")
                file.write(out_text_buff)
                file.close()    # print()
                break

        except UnicodeDecodeError as exc:
            print(' Error : ' + encoding_t)
            continue



