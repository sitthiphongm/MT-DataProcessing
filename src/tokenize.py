from pythainlp.tokenize import word_tokenize as word_tokenize_th
import deepcut
from nltk.tokenize import TweetTokenizer
import re

def tokenize_thai(text):
    tokens = deepcut.tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        # print(word)
        # word1=re.sub(r'([0-9]+)[ ]([.|,])[ ]([0-9]+)', r'\1\2\3', word)
        content_buff = content_buff + " " + word

    content_buff = ' '.join(content_buff.split())
    return( content_buff.strip() )

# Tokenize.
word_tokenize = TweetTokenizer()
def tokenize_eng(text):
    tokens = word_tokenize.tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        content_buff = content_buff + " " + word
    content_buff = ' '.join(content_buff.split())
    content_buff = re.sub(r"([a-zA-Z0-9])(\')([a-zA-Z0-9])", r'\1 \2\3', content_buff)
    return( content_buff.strip() )

# Tokenize.
'''
word_tokenize = TweetTokenizer()
def tokenize_eng(text):
    tokens = word_tokenize.tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        content_buff = content_buff + " " + word
    content_buff = ' '.join(content_buff.split())
    return( content_buff.strip() )
'''