import re

# http://jrgraphix.net/research/unicode.php
def language_not_en(text):
    for char in text:
        # basic latin
        if u'\u0020' <= char <= u'\u007F':
            continue
        # number
        if u'\u2150' <= char <= u'\u218F':
            continue
        print(text)
        return True
    return False

def language_not_th_en(text):
    for char in text:
        # basic latin
        if u'\u0020' <= char <= u'\u007F':
            continue
        # thai
        if u'\u0E00' <= char <= u'\u0E7F':
            continue
        # number
        if u'\u2150' <= char <= u'\u218F':
            continue
        print(text)
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