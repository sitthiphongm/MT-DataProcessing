import sys
import os
import codecs
from src.globalSetting import *

def loadThaiDictionay():
    dictionaryThai = {}
    with codecs.open(dictionary_thai, "r", encoding=encode_type) as dictFile:
        for line in dictFile.readlines():
            dictionaryThai[line.strip()] = 0
    return dictionaryThai

