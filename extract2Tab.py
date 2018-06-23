#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import re
import os
import glob
import sys
from langdetect import detect
from src.cleantext import clean_content
from src.cleantext import find_between_r

encode_type="UTF-8"
encode_type_en="UTF-8"
encode_type_th="TIS-620"

data_path = os.path.dirname(os.path.realpath(__file__))
data_path = data_path + '/data/unicode/*.en'
en_files = glob.glob(data_path)

# Process tabpair.
pair_buffer={}

progress=0
totol_files = len(en_files)
# sys.exit()

for source_file in en_files:
    # print(source_file)
    progress=progress+1
    if (progress%50 == 0):
        print((progress*100) / totol_files)
    out_text_buff=''

    try:
        with codecs.open(source_file, "r", encoding=encode_type) as sourceFile:
            for line in sourceFile.readlines():
                time_frame = find_between_r(line, 'Marked=', 'Default')
                time_frame = ((time_frame.lstrip(',')).strip(',')).strip()
                if (time_frame != ''):
                    key = re.sub('[^A-Za-z0-9]+', '', time_frame)
                    content = clean_content(line, 'en')
                    if(content != ''):
                        pair_buffer[key] = content

        # find target file name
        file_name = source_file.strip('.en')
        current_file_ext = source_file.find('.en')
        while (current_file_ext != -1):
            temp_file_ext = source_file.find('.en', current_file_ext + 1)
            if (temp_file_ext == -1):
                break
            current_file_ext = temp_file_ext

        file_name = source_file[0:current_file_ext]
        target_file = file_name + '.th'

        # print(target_file)

        with codecs.open(target_file, "r", encoding=encode_type) as targetFile:
            for line in targetFile.readlines():
                time_frame = find_between_r(line, 'Marked=', 'Default')
                time_frame = ((time_frame.lstrip(',')).strip(',')).strip()
                if (time_frame != ''):
                    key = re.sub('[^A-Za-z0-9]+', '', time_frame)
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

                        # wrong pair.
                        if (out_text != ''):
                            out_text_buff += out_text + '\n'
        filename_tab = file_name + '.tab'
        file = codecs.open(filename_tab, "w", "utf-8")
        file.write(out_text_buff)
        file.close()

    except FileNotFoundError:
        print('ERROR : File not found...')
