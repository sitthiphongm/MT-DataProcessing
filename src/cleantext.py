import re
import codecs
from src.language import language_not_en
from src.language import language_not_th_en

def describe(self, text):
    self.description = text

def authorName(self, text):
    self.author = text

encode_type="UTF-8"
encode_type_en="UTF-8"
encode_type_th="TIS-620"
encode_type=['TIS-620','UTF-8','LATIN-1','ISO-8859-1','ISO-8859-7', 'ISO-8859-5','ISO-8859-8']
def find_encoding(source_file):
    current_encode = False
    for encoding_t in encode_type:
        try:
            with codecs.open(source_file, "r", encoding=encoding_t) as decodeFile:
                decodeFile.readlines();
                current_encode = encode_type_en
                break
        except UnicodeDecodeError as exc:
            continue
    return current_encode

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""

def extract_between(source, start_sep, end_sep):
    result = []
    outtext = ''
    tmp = source.split(start_sep)
    for par in tmp:
        if end_sep in par:
            result.append(par.split(end_sep)[0])
    for word in result:
        outtext += ' ' + word
    # print(source)
    # print(' '.join(outtext.split()))
    return (outtext)

def remove_edge(text, start, end):
    text = text.strip()
    if text=='':
        return ''
    if text[0]==start:
        ending_point = text.find(end)
        # print(ending_point)
        if text[ending_point]==end:
            # print(text)
            text = text[1:ending_point]
            # print('     :' + text + ':')
    return text

def remove_between(text, start, end):
    text = text.strip()
    out_text=''
    if text=='':
        return False
    starting_point = text.find(start)
    # print(text)
    if  starting_point!=-1:
        ending_point = text.find(end)
        # print(starting_point)
        if ending_point!=-1:
            # print(ending_point)
            if (starting_point==0):
                out_text = text[ending_point+len(end):]
            else:
                # print( str( starting_point) + ' : ' + str(ending_point) + ' : ' + str(len(end)) )
                out_text = text[0:starting_point] + text[ending_point+len(end):]

            # print('     :' + out_text + ':')
            return out_text

    return False

def clean_content(text, lang):
    # space = ''
    if lang=='en':
        space=' '
    elif lang=='th':
        space = ''

    # TODO. We should not just remove \n. Need to do sentence segment.
    content = find_between_r(text, ',,', '\n')
    content = content.replace('\\n', '_SIG_NEWLINE_')
    content = content.replace('\\N', '_SIG_NEWLINE_')
    content = content.replace('//N', '_SIG_NEWLINE_')
    content = content.replace('/N', '_SIG_NEWLINE_')
    content = content.replace('...', '_SIG_JOINLINE_')
    # content = content.replace('..', '_SIG_JOINLINE_')

    # Clean tag.
    print(content)
    repeat=0
    while ((content.find('{') != -1) or (content.find('<') != -1)) and (repeat<15):
        repeat = repeat + 1
        content = re.sub(r'<.*?>', '', content)
        content = re.sub(r'{.*?}', '', content)
        content = re.sub(r'{[\\][a-zA-Z]{1}[0-9]{0,2}|[>][\/][\/][<]', '', content)
    print("====>",content)

    # Trim.
    content_s = remove_edge(content, '}', '{')
    if (content_s != ''):
        content = content_s
    content_s = remove_edge(content, '[', ']')
    if (content_s != ''):
        content = content_s
    content_s = remove_edge(content, '>', '<')
    if (content_s != ''):
        content = content_s
    content_s = remove_edge(content, '(', ')')
    if (content_s != ''):
        content = content_s

    content_s = remove_edge(content, '\\i0', '\\i1')
    if (content_s != ''):
        content = content_s
    content_s = extract_between(content, '\\j0', '\\j1')
    if (content_s != ''):
        content = content_s

    # Normoalize / Repalce bad char/string.
    # alot more bad char TODO here.
    content = content.replace('', "'")
    content = content.replace('', '"')
    content = content.replace('', '"')
    content = content.replace('', "'")

    content = content.replace('โ','"')
    content = content.replace('โ', '"')
    content = content.replace('โ', "'")
    content = content.replace('เน','e')
    content = content.replace('โช', '')
    content = content.replace('âª','#')

    # Clean.
    content = content.replace('♪', '')
    content = content.replace('♥', '')
    content = content.replace('­', '')
    content = content.replace('♫', '')
    content = content.replace('～', '')

    # Strp head / tail.
    content = content.lstrip('-')
    content = content.lstrip('"')
    content = content.replace('\\', '')
    content = content.strip()
    content = ' '.join(content.split())

    # check language
    if ((lang=='en') and (language_not_en(content)) ):
        return ''
    elif ((lang=='th') and (language_not_th_en(content)) ):
        return ''
    else:
        return content