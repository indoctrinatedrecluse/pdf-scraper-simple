# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 23:08:30 2023

@author: Abhishek Mitra
"""

# import the necessary libraries
import urllib
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.parse import urljoin
import os
import sys

# read the url from the console or seed file
try:
    url = sys.argv[1]
except IndexError:
    try:
        file = open('seeds.txt')
        url = file.readline()
    except Exception:
        url = 'https://www.math.hkust.edu.hk/excalibur/excalibur.htm'
if not url.startswith('http'):
    url = 'https://www.math.hkust.edu.hk/excalibur/excalibur.htm'
    
# download and parse the seed url in BeautifulSoup
soup = BeautifulSoup(urllib.request.urlopen(url))


all_link = soup.find_all('a') 
A=[]
B=[]
for link in all_link:
    A.append(link.contents[0])
    B.append(urljoin(url, link['href']))

df=pd.DataFrame(A, columns = ['Description'])
df['link'] = B


dirname = os.path.dirname(__file__)
relpath = 'output'
path = os.path.join(dirname, relpath, 'output.csv')
if not os.path.exists(relpath):
    os.makedirs(relpath)
df.to_csv(path)


for link in B:
    file_name = link.split('/')[-1]

    # just a sanity test for link
    try:
        u=urllib.request.urlopen(link)
    except urllib.error.URLError as e:
        print(e.reason)
        continue
    
    # skip non-pdfs
    meta = u.info()
    if(meta['Content-Type'] != 'application/pdf'):
        continue
        
    # set absolute path for the file
    path_file_name = os.path.join(dirname, relpath, file_name)
        
    # download file using fixed buffer
    f = open(path_file_name, 'wb')
    file_size=int(meta['Content-Length'])
    print(f"Downloading: %s Bytes: %s" % (file_name, file_size))
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print (status)
    print("\n\nFIN!")
    f.close()