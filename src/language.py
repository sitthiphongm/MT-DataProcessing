import re

# http://jrgraphix.net/research/unicode.php

def special_char(char):
    if re.match('[\u0020-\u0040\u005B-\u0060\u007B-\u007E]', char):
        return True
    elif re.match('[\u00A9\u00AE\u2122\u00B0\u2103\u2109]', char):
        return True
    elif re.match('[\u0024\u00A2-\u00A5\u058F\u060B\u09F2\u09F3\u09FB\u0AF1\u0BF9\u0E3F\u17DB\u20A0-\u20AF\u20B0-\u20BE\uA838\uFDFC\uFE69\uFF04\uFFE0\uFFE1\uFFE5\uFFE6]', char):
        return True
    elif re.match('[\u00B1\u00B5\u03BC\u2126\u2265\u2264\u00B2\u00BD\u00D7\u03B2\u0392\u00B3\u03C0\u03B1\u03B8\u03D5\u00BC\u03B4\u03C9\u00DF\u03BB\u0394\u00F7\u2206\u03A9\u03BA\u03B3\u2261\u03A3\u03C3\u03C6\u2211\u03B5\u03C1\u00A7\u0398\u03C4]', char):
        return True
    elif re.match('[\u0009]', char):
        return True
    else:
        return False

def language_not_en(text):
    for char in text:
        if u'\u0020' <= char <= u'\u007E': # basic latin
            continue
        elif u'\u2150' <= char <= u'\u218F': # number
            continue
        elif special_char:
            continue
        print("remove text : " + text)
        return True
    return False

def language_not_enth(text):
    for char in text:
        if u'\u0E01' <= char <= u'\u0E5B': # thai
            continue
        elif u'\u2150' <= char <= u'\u218F': # number
            continue
        elif u'\u0020' <= char <= u'\u007E': # basic latin
            continue
        elif special_char:
            continue
        print("remove text : " + text)
        return True
    return False

def language_mixed_en(text):
    if re.match("[a-zA-Z]+", text):
        return True
    else:
        return False
def language_no_th_char(text):
    if (re.search(r'[ก-ฮ]', text)):
        return False
    else:
        return True
def language_contain_en(text):
    if re.match("[a-zA-Z]+", text):
        return False
    else:
        return True
def language_mixed_th(text):
    if u'\u0E01' <= text <= u'\u0E5B':
        return True
    else:
        return False

# text = '2.6424733550603365'
# print(language_not_en(text))