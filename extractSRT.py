#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import re
import os
import glob
import sys
import time
from datetime import datetime
from langdetect import detect
from src.cleantext import *
from src.sentence import *

encode_type="UTF-8"
encode_type_en="UTF-8"
encode_type_th="TIS-620"

data_path = os.path.dirname(os.path.realpath(__file__))
data_path = data_path + '/data/srt/*.en'
en_files = glob.glob(data_path)

# Process tabpair.
pairBuffer={}
sourceBuffer={}
targetBuffer={}
sourceBufferTime={}
targetBufferTime={}

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

        print(source_file)
        # Do not process completed files.
        # file_name = source_file.strip('.en')
        # filename_tab = file_name + '.tab'
        # if os.path.exists(filename_tab):
        #   continue

        with codecs.open(source_file, "r", encoding=encode_type) as sourceFile:
            prev_content = ''
            count=0
            for line in sourceFile.readlines():
                time_frame = find_between_r(line, 'Marked=', 'Default')
                time_frame = ((time_frame.lstrip(',')).strip(',')).strip()
                content = clean_content(line, 'en')
                if (time_frame != ''):
                    # key = re.sub('[^A-Za-z0-9]+', '', time_frame)
                    # key = time_frame
                    if(content != ''):
                        sourceBuffer[count] = content
                        sourceBufferTime[count] = time_frame
                        count=count+1
                prev_content = content

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
            prev_content=''
            count = 0
            for line in targetFile.readlines():
                time_frame = find_between_r(line, 'Marked=', 'Default')
                time_frame = ((time_frame.lstrip(',')).strip(',')).strip()
                if (time_frame != ''):
                    # key = re.sub('[^A-Za-z0-9]+', '', time_frame)
                    # key = time_frame
                    content = clean_content(line, 'th')
                    if (content != ''):
                        targetBuffer[count] = content
                        targetBufferTime[count] = time_frame
                        count = count + 1
                prev_content = content

        out_text_buff=align_sentence(sourceBuffer, sourceBufferTime, targetBuffer, targetBufferTime)
        filename_tab = file_name + '.tab'
        file = codecs.open(filename_tab, "w", "utf-8")
        file.write(out_text_buff)
        file.close()

    except FileNotFoundError:
        print('ERROR : File not found...')
