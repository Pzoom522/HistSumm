#!/usr/bin/env python
# coding: utf-8

import os
import re
import linecache
import pathlib
import tqdm
import shutil
import jieba
import opencc
from utils.regu import filter_marked_sentences
from utils.regu import filter_mlmarked_sentences
from utils.regu import end_token
from jiayan import load_lm
from jiayan import CRFPunctuator
from hanziconv import HanziConv

chinese_regex = re.compile('[\u4e00-\u9fa5]|[\u3400-\u4db5]')

def make_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    

def get_all_files(root):
    file_names = os.listdir(root)
    file_ob_list = []
    
    # mac特殊文件
    for file_name in file_names:
        if file_name != ".DS_Store":
            file_ob_list.append(file_name)
   
    return file_ob_list


def cut_sentences(para):
    para = re.sub(r"([。！；？\!\?\.．…;:])\1+", r"\1", para)
    para = re.sub('([。！；？\!\?\.．…;:])([^”’」』])', r"\1\n\2", para)
    para = re.sub('(\.{6})([^”’」』])', r"\1\n\2", para)
    para = re.sub('(\…{2})([^”’」』])', r"\1\n\2", para)
    para = re.sub('([。！；？\!\?\.．…;:][”’」』])([^，。！；？\!\?\.．…;:])', r'\1\n\2', para)
    para = para.rstrip() 
    sentences = para.split("\n")
    sentences = [sent for sent in sentences if len(sent.strip()) > 0]

    return sentences


def process_file(root, target_root, marked): 
    for f_name in (get_all_files(root)):
        output = open(target_root + f_name, "w+", encoding='utf-8-sig', errors='ignore')
        with open(root + f_name, "r", encoding='utf-8-sig',errors='ignore') as f:
            for l in f.readlines():
                if len(l.strip()) == 0:
                    continue
                for part in cut_sentences(l.strip()):
                    if marked:
                        filtered = filter_marked_sentences(part.strip())
                    else:
                        filtered = filter_mlmarked_sentences(part.strip())
                    if len(filtered) > 0:
                        output.write(filtered)
                        output.write("\n")  
        output.close()
        
        
def tag_text(root, target_root):
    # jiayan ancient text cut tool
    lm = load_lm('jiayan.klm')
    punctuator = CRFPunctuator(lm, 'cut_model')
    punctuator.load('punc_model')
            
    make_dir(target_root)
    file_ob_list = get_all_files(root)
    for f_name in tqdm.tqdm(file_ob_list, desc="Process unmarked file"):
        file = open(root + f_name, "r", encoding='utf-8-sig',errors='ignore')
        output = open(target_root + f_name, "w+", encoding='utf-8-sig', errors='ignore')
        for line in file.readlines():
            if len(line.strip()) == 0:
                continue
            output.write(punctuator.punctuate(line.strip()))
            output.write('\n')
        file.close()
        output.close()

                
def merge_files(root, root2, target):
    file_names = get_all_files(root)
    output = open(target, "w+", encoding='utf-8', errors='ignore')
    for file_name in tqdm.tqdm(file_names, desc="merge all files in root folder:"):
        f = open(root + file_name, "r", encoding='utf-8',errors='ignore')
        for line in f.readlines():
            if line != None and line != ' ':
                line = line.replace('@+', '@')
                line = line.replace('@', ' ')
                output.write(line)
                # output.write('\n')
        f.close()
        
    file_names = get_all_files(root2)
    for file_name in tqdm.tqdm(file_names, desc="merge all files in root folder:"):
        f = open(root2 + file_name, "r", encoding='utf-8',errors='ignore')
        for line in f.readlines():
            if line != None and line != ' ':
                line = line.replace('@+', '@')
                line = line.replace('@', ' ')
                output.write(line)
                # output.write('\n')
        f.close()
    output.close()            
    

def separate_words(input_folder, target_file):
    converter = opencc.OpenCC('s2t.json')
    target = open(target_file, "w+", encoding='utf-8-sig', errors='ignore')
    
    all_count = 0
    count = 0
    for file in tqdm.tqdm(get_all_files(input_folder), desc="cut sentences"):
        with open(input_folder + file, "r", encoding='utf-8-sig', errors='ignore') as f:
            text = f.readlines()
            for sen in text:
                sentence = converter.convert(sen.strip())
                #sentence = sen.strip()
                if len(sentence) == 0:
                    continue
                elif len(sentence) >= 10:
                    count += 1
                all_count += 1
                for word in sentence:
                    target.write(word)
                    target.write(' ')
                
                target.write('\n')
            del text
    target.close()
    print("All sentences: " + str(all_count))
    print("Sentences contain more than 10 words: " + str(count))