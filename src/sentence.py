import re
from nltk.tokenize import sent_tokenize as split_sentence_en
import time
from datetime import datetime
from src.globalSetting import *

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
        # nothing to do
        pass
    elif (len(sourceSentence) == len(targetSentence)):
        # nothing to do
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

        '''
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
        '''

    en_ss=' '.join([str(x) for x in sourceSentence])
    th_ss = ' '.join([str(x) for x in targetSentence])

def joint_sentence(sourceBuffer, sourceBufferTime):
    # FMT = '%H:%M:%S'
    # FMT = '%H:%M:%S.%f';
    # Joint Sentence
    t1 = '0:00:00.00';
    t2 = '0:00:00.00';
    prev_t1 = '0:00:00.00';
    prev_t2 = '0:00:00.00'
    prev_conversion = ''
    for key, time in sourceBufferTime.items():
        if sourceBuffer[key] != '':
            offset = 0
            numjoint = sourceBuffer[key + offset].find('_SIG_JOINLINE_')
            if (numjoint != -1):

                # current time.
                print("==>")
                print(numjoint)

                print('org text  : ', sourceBuffer[key + offset])
                try:
                    print('merge to  : ', sourceBuffer[key + offset + 1])
                except:
                    pass

                curr_text = sourceBuffer[key + offset].replace('_SIG_JOINLINE_', '')
                next_text_idx=key+offset+1
                if next_text_idx >= len(sourceBuffer):
                    continue

                next_text = sourceBuffer[key + offset + 1]
                time_tkns = time.split(',')
                t0 = time_tkns[0]
                t1 = time_tkns[1]
                t2 = time_tkns[2]

                # next time.
                time_next = sourceBufferTime[key + offset + 1]
                time_next_tkns = time_next.split(',')
                t1_next = time_next_tkns[1]
                t2_next = time_next_tkns[2]

                if t2=='Default':
                    t2=t1
                if t2_next=='Default':
                    t2_next=t1_next

                # diff time.

                try:
                    tdelta = datetime.strptime(t1_next, FMT) - datetime.strptime(t2, FMT)
                except:
                    print(time, t1_next, t2)
                    print(time_next)
                    continue

                seconddiff = str(tdelta).split(':')
                seconddiff = seconddiff[-1]
                timediff = float(seconddiff)
                print("diff time : ", timediff)

                if next_text=='':
                    pass
                # elif (re.search(r'[A-Z]', next_text[0])):
                #    sourceBuffer[key + offset] = ''
                elif (timediff < JOIN_MSEC_DIFF):
                    # print('source :', sourceBuffer[key+next])
                    # print('joint  :', sourceBuffer[key+next+1])
                    # print('time diff  :', timediff)
                    # print('\n')
                    # jointable.
                    sourceBuffer[key + offset] = ''
                    sourceBuffer[key + offset + 1] = curr_text + sourceBuffer[key + offset + 1]
                    print('text merge : ', sourceBuffer[key + offset + 1])
                    print(sourceBufferTime[key + offset])
                    sourceBufferTime[key + offset + 1] = str(t0) + ',' + str(t1) + ',' + str(t2_next)
                    print('time merge : ', sourceBufferTime[key + offset + 1])

                else:
                    # through away.
                    sourceBuffer[key + offset] = ''
                    sourceBuffer[key + offset + 1] = ''

    # return (sourceBuffer, sourceBufferTime)

def joinable(sourceBuffer, sourceBufferTime, index):
    # current time.
    if index >= len(sourceBuffer):
        return False
    next_text_idx = index + 1
    if next_text_idx >= len(sourceBuffer):
        curr_text = sourceBuffer[index].replace('_SIG_JOINLINE_', '')
        return False

    curr_text = sourceBuffer[index].replace('_SIG_JOINLINE_', '')
    # print("==>", index)
    # print('org text  : ', sourceBuffer[index])
    # try:
        # print('merge to  : ', sourceBuffer[index + 1])
    # except:
    #     pass

    time = sourceBufferTime[index]
    next_text = sourceBuffer[index + 1]
    time_tkns = time.split(',')
    t0 = time_tkns[0]
    t1 = time_tkns[1]
    t2 = time_tkns[2]

    # next time.
    time_next = sourceBufferTime[index + 1]
    time_next_tkns = time_next.split(',')
    t1_next = time_next_tkns[1]
    t2_next = time_next_tkns[2]

    if t2 == 'Default':
        t2 = t1
    if t2_next == 'Default':
        t2_next = t1_next

    # diff time.
    try:
        tdelta = datetime.strptime(t1_next, FMT) - datetime.strptime(t2, FMT)
    except:
        print(time, t1_next, t2)
        print(time_next)
        return False

    seconddiff = str(tdelta).split(':')
    seconddiff = seconddiff[-1]
    timediff = float(seconddiff)
    # print("diff time : ", timediff)

    if next_text == '':
        pass
    elif (re.search(r'[A-Z]', next_text[0])):
        sourceBuffer[index] = ''
    elif (timediff < JOIN_MSEC_DIFF):
        # print('source :', sourceBuffer[key+next])
        # print('joint  :', sourceBuffer[key+next+1])
        # print('time diff  :', timediff)
        # print('\n')
        # jointable.
        sourceBuffer[index] = ''
        sourceBuffer[index + 1] = curr_text + sourceBuffer[index + 1] + '__JOINT__'
        # print('text merge : ', sourceBuffer[index + 1])
        # print(sourceBufferTime[index])
        sourceBufferTime[index + 1] = str(t0) + ',' + str(t1) + ',' + str(t2_next)
        # print('time merge : ', sourceBufferTime[index + 1])

    else:
        # through away.
        sourceBuffer[index] = ''
        sourceBuffer[index + 1] = ''

def align_sentence(sourceBuffer, sourceBufferTime, targetBuffer, targetBufferTime):
    out_text_buff = ''
    ROUNDING_TRESHOLD = 25
    out_text_buff = ''

    # joint_sentence(sourceBuffer, sourceBufferTime)
    # joint_sentence(targetBuffer, targetBufferTime)

    diff_threshold = datetime.strptime(DIFF_START_TRESHOLD, FMT) - datetime.strptime('00:00:00.0', FMT)
    diff_dummy = datetime.strptime(DIFF_START_DUMMAY, FMT) - datetime.strptime('00:00:00.0', FMT)

    for index, time in sourceBufferTime.items():
        rounding = 0
        if sourceBuffer[index] != '':
            while rounding <= ROUNDING_TRESHOLD:
                source_time_tkns = time.split(',')
                t1_source = source_time_tkns[1]

                # forward.
                index_rounding = index + rounding
                if ((index_rounding < len(targetBufferTime)) and index_rounding >= 0):
                    target_time_tkns = targetBufferTime[index_rounding].split(',')
                    t1_target = target_time_tkns[1]
                    # print(t1_source, t1_target)
                    if t1_source >= t1_target:
                        try:
                            tdelta = datetime.strptime(t1_source, FMT) - datetime.strptime(t1_target, FMT)
                        except:
                            print('time format error', time, targetBufferTime[index_rounding])
                            tdelta = diff_dummy
                            pass
                    elif t1_source < t1_target:
                        try:
                            tdelta = datetime.strptime(t1_target, FMT) - datetime.strptime(t1_source, FMT)
                        except:
                            print('time format error', time, targetBufferTime[index_rounding])
                            tdelta = diff_dummy
                            pass
                    else:
                        print('error')

                    # print(t1_source, t1_target)

                    if (tdelta < diff_threshold):
                        # print('=>', tdelta, DIFF_START_TRESHOLD)
                        if targetBuffer[index_rounding] != '':
                            active_index=index
                            join=False
                            while (sourceBuffer[active_index].find('_SIG_JOINLINE_') != -1):
                                joinable(sourceBuffer, sourceBufferTime, active_index)
                                joinable(targetBuffer, targetBufferTime, active_index+rounding)
                                active_index=active_index+1
                                join=True
                            if join==False:
                                out_text_buff = out_text_buff + sourceBuffer[active_index] + '\t' + targetBuffer[active_index+rounding] + '\n'
                            break

                # backward.
                index_rounding = index - rounding
                if ((index_rounding < len(targetBufferTime)) and index_rounding >= 0):
                    target_time_tkns = targetBufferTime[index_rounding].split(',')
                    t1_target = target_time_tkns[1]
                    # print(t1_source, t1_target)
                    if t1_source >= t1_target:
                        try:
                            tdelta = datetime.strptime(t1_source, FMT) - datetime.strptime(t1_target, FMT)
                        except:
                            print('time format error', time, targetBufferTime[index_rounding])
                            tdelta = diff_dummy
                            pass
                    elif t1_source < t1_target:
                        try:
                            tdelta = datetime.strptime(t1_target, FMT) - datetime.strptime(t1_source, FMT)
                        except:
                            print('time format error', time, targetBufferTime[index_rounding])
                            tdelta = diff_dummy
                            pass
                    else:
                        print('error')

                    if (tdelta < diff_threshold):
                        # print('=>', tdelta, DIFF_START_TRESHOLD)
                        if targetBuffer[index_rounding] != '':
                            active_index=index
                            join=False
                            while (sourceBuffer[active_index].find('_SIG_JOINLINE_') != -1):
                                joinable(sourceBuffer, sourceBufferTime, active_index)
                                joinable(targetBuffer, targetBufferTime, active_index-rounding)
                                active_index=active_index+1
                                join = True
                            if join==False:
                                out_text_buff = out_text_buff + sourceBuffer[active_index] + '\t' + targetBuffer[active_index-rounding] + '\n'
                            break

                rounding = rounding + 1

    return(out_text_buff)