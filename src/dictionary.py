import sys
import os
import codecs
from src.globalSetting import *

def loadThaiDictionary():
    dictionaryThai = {}
    with codecs.open(dictionary_tha, "r", encoding=encode_type) as dictFile:
        for line in dictFile.readlines():
            dictionaryThai[line.strip()] = 0
    return dictionaryThai

def loadDictionary():
    dictionaryThai = {}
    with codecs.open(dictionary_tab, "r", encoding=encode_type) as dictFile:
        for line in dictFile.readlines():
            tokens = line.split('\t')
            dictionaryThai[tokens[1].strip()] = tokens[0].strip()
    return dictionaryThai

def createHunDictionary():
    dictionaryTab = {}
    open(dictionary_hun, 'w').close()
    with codecs.open(dictionary_tab, "r", encoding=encode_type) as dictFile:
        line_count=0
        content_buff = ""
        for line in dictFile.readlines():
            tokens=line.strip().split('\t')
            content_buff=content_buff + tokens[1] + ' ' + '@' + ' ' + tokens[0] + '\n'
            line_count=line_count+1
            if (line_count%10000 == 0):
                file = codecs.open(dictionary_hun, "a", encode_type)
                file.write(content_buff)
                file.close()
                content_buff = ""
        # Write last chunk.
        file = codecs.open(dictionary_hun, "a", encode_type)
        file.write(content_buff)
        file.close()
        content_buff = ""
