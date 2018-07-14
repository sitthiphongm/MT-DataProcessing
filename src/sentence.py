import re
from nltk.tokenize import sent_tokenize as split_sentence_en


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
                    # TODO, add bug fix here and to test.
                    idx = idx + 1
            else:
                if (sentence != ""):
                    new_sense.append(sentence)
                    idx=idx+1

        prev_sense=sentence

    return new_sense

def detok_thai(text, dictionary):
    # text = ' '.join(text.split())
    tokens = text.split()
    if len(tokens)<2:
        return text

    # Joint sentence.
    new_sense=[]
    prev_sense=""
    idx=0
    for curr_sense in tokens:
        # print("--",prev_sense)
        if (re.search(r'[0-9๐-๙]', prev_sense)):
            new_sense[idx-1] = new_sense[idx-1] + " " + curr_sense
        elif (re.search(r'[a-zA-Z]', prev_sense)):
            # print(curr_sense[0])
            if (re.search(r"[']", curr_sense[0])):
                new_sense[idx - 1] = new_sense[idx - 1] + curr_sense
            else:
                if (curr_sense != ""):
                    new_sense.append(curr_sense)
                    idx = idx + 1
        elif (re.search(r'[,|!|ๆ]$', prev_sense)):
            new_sense[idx-1] = new_sense[idx-1] + " " + curr_sense
        else:
            if (idx == 0):
                new_sense.append(curr_sense)
                idx = idx + 1
                prev_sense = curr_sense
                continue

            if (re.search(r'[0-9๐-๙|ๆ|ฯ]', curr_sense)):
                new_sense[idx-1] = new_sense[idx-1] + " " + curr_sense
            # elif curr_sense in dictionary and prev_sense in dictionary:
            # Re-TOK case.
            # elif curr_sense in dictionary:
            elif (re.search(r'[ก-ฮ|เ-ไ|/|)|(|\]|\[|\}|\{|\"]', curr_sense[0])):
                new_sense[idx-1] = new_sense[idx-1] + curr_sense
            else:
                if (curr_sense != ""):
                    new_sense.append(curr_sense)
                    idx=idx+1

        prev_sense=curr_sense

    outtext =' '.join([str(x) for x in new_sense])

    return outtext

def get_error(source_len, target_len):
    error = (int)(100 * abs(target_len-source_len) / ( target_len + source_len ) )
    return error

def is_end(active_idx, sourceLen, targetLen):
    if (active_idx >= len(sourceLen) or active_idx >= len(targetLen)):
        return True
    else:
        return False

def aplign_pair(en_ss, th_ss, max_error, forward):

    sourceSentence = split_sentence_en(en_ss)
    targetSentence = split_sentence_th(th_ss)

    if (len(sourceSentence) == 1 or len(targetSentence) == 1):
        # TODO
        pass
    elif (len(sourceSentence) == len(targetSentence)):
        # TODO
        pass
    else:
        # Character ratio
        ratio = len(en_ss) / len(th_ss)

        # print('\n :::::: ' + str(ratio))

        targetLen = targetSentence[:]
        for i in range(len(targetLen)):
            num_char = len(targetSentence[i])
            if (ratio > 1):
                targetLen[i] = (int)(num_char * ratio)
            else:
                targetLen[i] = num_char

        sourceLen = sourceSentence[:]
        for i in range(len(sourceLen)):
            num_char = len(sourceSentence[i])
            if (ratio < 1):
                sourceLen[i] = (int)(num_char * ratio)
            else:
                sourceLen[i] = num_char

        # print(sourceSentence)
        # print(sourceLen)
        # print(targetSentence)
        # print(targetLen)

        # Normal case.
        if forward:
            active_idx = 0
        else:
            active_idx = len(sourceLen)

        while len(sourceLen) < len(targetLen):
            prev_error = get_error(sourceLen[active_idx], targetLen[active_idx])
            if (prev_error <= max_error):
                break;
            diff_len = abs(len(sourceSentence) - len(targetSentence))
            new_error = 100
            while new_error >= max_error:
                if (diff_len > 0):
                    if is_end(active_idx, sourceLen, targetLen):
                        break
                    # Try to get merged text len.
                    merge_text_len = targetLen[active_idx] + targetLen[active_idx + 1]
                    new_error = get_error(sourceLen[active_idx], merge_text_len)
                    # if the merge seems reduce error then go.
                    if (new_error < prev_error):
                        # Combine len.
                        targetSentence[active_idx] = targetSentence[active_idx] + targetSentence[active_idx + 1]
                        del targetSentence[active_idx + 1]
                        # Combine text.
                        targetLen[active_idx] = merge_text_len
                        del targetLen[active_idx + 1]
                        # Getting new error.
                        prev_error = new_error
                        diff_len = len(targetSentence) - len(sourceSentence)
                        # Stay on th ecurrent index.
                    else:
                        # Go to the next index & try merge futhur.
                        active_idx = active_idx + 1
                        break
                else:
                    active_idx = active_idx + 1
                    break

            if is_end(active_idx, sourceLen, targetLen):
                break

        if len(sourceLen) == len(targetLen):
            print(sourceSentence)
            print(sourceLen)
            print(targetSentence)
            print(targetLen)
        else:
            print("FFFFFFFFFFFFFFFFF")
            print(sourceSentence)
            print(sourceLen)
            print(targetSentence)
            print(targetLen)


# def combine_sentence(text):
