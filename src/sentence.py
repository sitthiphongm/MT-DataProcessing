import re

def split_sentence_th(text):
    # print("-------", text)
    tokens = text.split()
    if len(tokens)<2:
        return [text]

    # Joint sentence.
    new_sense=[]
    prev_sense=""
    idx=0
    for sentence in tokens:
        if (re.search(r'[0-9๐-๙]', prev_sense)):
            new_sense[idx-1] = new_sense[idx-1] + " " + sentence
        elif (re.search(r'[,|!|ๆ|]$', prev_sense)):
            new_sense[idx-1] = new_sense[idx-1] + " " + sentence
        else:
            if (re.search(r'[0-9๐-๙|ๆ|ฯ]', sentence)):
                if (idx>0):
                    new_sense[idx-1] = new_sense[idx-1] + " " + sentence
                else:
                    new_sense.append(sentence)
            else:
                if (sentence != ""):
                    new_sense.append(sentence)
                    idx=idx+1


        prev_sense=sentence

    return new_sense

# def combine_sentence(text):
