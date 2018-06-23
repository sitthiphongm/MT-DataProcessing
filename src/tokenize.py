from nltk.tokenize import word_tokenize
from pythainlp.tokenize import word_tokenize as word_tokenize_th

def tokenize_eng(text):
    tokens = word_tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        content_buff = content_buff + " " + word
    content_buff = ' '.join(content_buff.split())
    return( content_buff.strip() )

def tokenize_thai(text):
    tokens = deepcut.tokenize(text)
    # return ' '.join(pieces)
    content_buff = ""
    for word in tokens:
        content_buff = content_buff + " " + word
    content_buff = ' '.join(content_buff.split())
    return( content_buff.strip() )
