#!/usr/bin/env python
# coding: utf-8
import csv
import re
import os
from tqdm import tqdm

def get_all_files(root):
    file_names = os.listdir(root)
    file_ob_list = []
    for file_name in file_names:
        if file_name != ".DS_Store":
            file_ob_list.append(file_name)
   
    return file_ob_list


sign = ['.','/',',',':','-','(',')',"\"",'\'',';','?','!']
sig = ['/',',',':','(',')',"\"",'\'',';','?','!']

def process_sentence(line):
    s = re.sub("/",',',line)

    words = s.split()
    pre = ''

    for i in words:
        # a-abc conditions
        if '-' in pre and len(re.sub("-","",pre)) != 0:
            if len(pre.split('-')) == 2:
                word1 = pre.split('-')[0]
                word2 = pre.split('-')[1]
                if word1 in word2:
                    print(pre)               
        pre = i
    for i in sig:
        s = s.replace(i,' '+i)
    return s


def process(word):
    s = word
    s = re.sub(r'[^a-zA-Z0-9.]',' ',s)
    s = re.sub('[oͤuͤaͤ]','',s)
    return s

    
def merge_files(root, target):
    file_names = get_all_files(root)
    output = open(target, "w+", encoding='utf-8-sig', errors='ignore')
    for file_name in tqdm(file_names, desc="merge all files in root folder:"):
        f = open(root + file_name, "r", encoding='utf-8-sig',errors='ignore')
        for line in f.readlines():
            l = line.strip()
            if len(l) == 0 or l == '\n':
                continue
            output.write(l)
            output.write('\n')
        f.close()
    output.close()