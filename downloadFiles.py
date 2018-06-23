#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import re
import os
import urllib
from requests import get
from io import BytesIO
from zipfile import ZipFile

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
PER_PAGE=20
MAX_PAGE=26650
BLOCKSIZE = 1048576
pange_number=1
skip=1

def dowload_file(download_path, org_name, use_name , encode_type):
    request = get(download_path)
    zip_file = ZipFile(BytesIO(request.content))
    files = zip_file.namelist()
    subtitle_file = files[0]

    # Reading the first file in the zip file:
    org_name = "data/original/" + org_name
    use_name = "data/unicode/" + use_name

    with open(org_name, "wb") as subtitle_buf:
        subtitle_buf.write( zip_file.read(files[0]) )

    '''
    if encode_type=="UTF-8":
        with open(use_name, "wb") as subtitle_buf:
            subtitle_buf.write(zip_file.read( subtitle_file ))
    else:
        with codecs.open(org_name, "r", encode_type) as sourceFile:
            with codecs.open(use_name, "w", "UTF-8") as targetFile:
                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)
    '''

while (pange_number < MAX_PAGE):
    url = 'http://www.thaisubtitle.com/manage/subtitle.php?start=' + str(pange_number) + '&name='
    print('URL : ' + url)
    html_response = urllib.request.urlopen(url)
    for line in html_response:
        line = line.decode('latin-1')
        if '"Complete"><br>100%' in line:
            k = line.find('<a href="download.php?')
            k = line.find('="', k)
            j = line.find('">', k)
            url_download = line[k+2:j]
            full_download_en = 'http://www.thaisubtitle.com/manage/' + url_download
            print(full_download_en)

            begin_text = 'alt="Download'
            n = line.find(begin_text)
            #n = line.find(' ', n)
            m = line.find('">', n)
            name_download = line[n+len(begin_text):m]
            name_download = str(name_download).strip()
            # name_download = re.sub(r"\s+", '-', name_download)
            # name_download = re.sub("[ ,.]", '-', name_download)

            a = full_download_en.find('=')
            b = full_download_en.find('&', a)
            dl_num = full_download_en[a+1:b]
            a = full_download_en.find('=',b)
            lang = full_download_en[a+1:]

            dl_use_name = str(dl_num + '.' + lang)
            dl_org_name = str(dl_num + '.' + re.sub('[^A-Za-z0-9]+', '', name_download) + '.' + lang)

            print(dl_org_name)
            dowload_file(full_download_en, dl_org_name, dl_use_name, 'UTF-8')

            k = j + 1
            k = line.find('<a href="download.php?', j)
            k = line.find('="', k)
            j = line.find('">', k)
            url_download = line[k+2:j]
            full_download_th = 'http://www.thaisubtitle.com/manage/' + url_download
            print(full_download_th)


            n = line.find('alt="Download', m)
            n = line.find(begin_text)
            #n = line.find(' ', n)
            m = line.find('">', n)
            name_download = line[n+len(begin_text):m]
            name_download = str(name_download).strip()
            # name_download = re.sub(r"\s+", '-', name_download)
            # name_download = re.sub("[ ,.]", '-', name_download)


            a = full_download_th.find('=')
            b = full_download_th.find('&', a)
            dl_num = full_download_th[a+1:b]
            a = full_download_th.find('=',b)
            lang = full_download_th[a+1:]

            dl_use_name = str(dl_num + '.' + lang)
            dl_org_name = str(dl_num + '.' + re.sub('[^A-Za-z0-9]+', '', name_download) + '.' + lang)
            # print(name_download)


            dowload_file(full_download_th, dl_org_name, dl_use_name, "TIS-620")

    pange_number = pange_number + PER_PAGE


