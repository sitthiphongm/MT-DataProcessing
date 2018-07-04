#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import os
import sys
import glob
from os.path import basename

encode_type="UTF-8"

dirname = sys.argv[-1]
dirname = dirname.strip()

if dirname[-1] != "/":
    dirname+="/"
# print(dirname)

to_data_path = dirname + '*.txt'
list_file=glob.glob(to_data_path)

for input_file in list_file:
    print(input_file)
    output_dir=os.path.dirname(input_file)+"/"
    base_name=str(basename(input_file)).split(".")
    base_name=base_name[0]
    output_file= output_dir + base_name + ".detok"
    content_buff=''

    # Empty file.
    open(output_file, 'w').close()

    content_buff=""

    with codecs.open(input_file, "r", encoding=encode_type) as sourceFile:
        line_count=0
        for line in sourceFile.readlines():
            # content = clean_content(line, ' ')
            line=line.strip()
            line = ' '.join(line.split())
            if(line==""):
                content_buff += line
                content_buff += "\n"
                continue
            tokens = line.split(" ");
            count_word=0
            len_word=len(tokens)
            join_word=1
            content_buff_temp="";

            # TODO on this for loop. Need chages to simple REGEX as sentence split did.
            for word in tokens:
                word=word.strip()
                if count_word < len_word:
                    # For Thai and Thai word joining
                    if u'\u0E01' <= word[0] <= u'\u0E4F':
                        if join_word==1 or join_word==2 or join_word==3:
                            content_buff_temp=content_buff_temp+word
                        else:
                            content_buff_temp = content_buff_temp + " " + word
                    # elif word[0]=="(" or word[0]=="[":
                    #     content_buff = content_buff + " " + word

                    # For Thai and NonEnglish word.
                    elif re.match("[^a-zA-Z0-9]+", word):
                        if join_word == 1:
                            content_buff_temp=content_buff_temp+word
                        elif join_word == 2:
                            content_buff_temp = content_buff_temp + word
                        else:
                            content_buff_temp = content_buff_temp + " " + word
                    else:
                        content_buff_temp = content_buff_temp + " " + word
                    # For Thai word
                    if u'\u0E01' <= word[-1] <= u'\u0E4F':
                        join_word = 1;
                    # Parenthesis
                    elif word[-1] == ")" or word[-1] == "]" or word[-1] == "}" or  word[-1]=="'" or  word[-1]=='"':
                        join_word = 2;
                    # Parenthesis
                    elif word[-1] == "(" or word[-1] == "[" or word[-1] == "{" or  word[-1]=="'" or  word[-1]=='"':
                        join_word = 2;
                    # None english word and number.
                    elif re.match("[^a-zA-Z0-9]+", word):
                        join_word = 3;
                        # print("-----" + word)
                    elif re.match("[a-zA-Z]+", word):
                        join_word = 5;
                        # print("-----" + word)
                    else:
                        join_word = 0;


            # RED dot/new line, replace with empty
            content_buff_temp=content_buff_temp.strip()
            content_buff_temp=re.sub(r"[\ ]@-@[\ ]|[\ ]@-@|@-@[\ ]", "-",content_buff_temp)
            content_buff_temp = re.sub(r'\s([\'!?\.,])', r'\1', content_buff_temp)

            ''' to cintunue
            content_buff_temp=re.sub(r'\s(["\'])', r'\1', content_buff_temp)
            content_buff_temp=re.sub(r'("|\')([\ ])', r'\1', content_buff_temp)
            content_buff_temp = re.sub(r'(")(")', r'\1 \2', content_buff_temp)
            content_buff_temp = re.sub(r'([a-zA-Z])([\ ])(\,|.)', r'\1\3', content_buff_temp)
            content_buff_temp=re.sub(r'\s([?.!"\'](?:\s|$))', r'\1', content_buff_temp)
            '''

            # print(content_buff_temp)
            content_buff=content_buff + content_buff_temp + "\n"

            line_count += 1
            # Flush data.
            if (line_count%10000 == 0):
                file = codecs.open(output_file, "a", "utf-8")
                file.write(content_buff)
                file.close()
                content_buff=""
                # print(line_count)

    # Write last chunk.
    file = codecs.open(output_file, "a", "utf-8")
    file.write(content_buff)
    file.close()
    content_buff=""
