#!/usr/bin/env python
# coding: utf-8

import os
import re
import linecache
import shutil
import json
import jieba
import xmltodict
import sys
import opencc
from tqdm import tqdm
from utils.regu import filter_sentences

CHINESE_REGEX = re.compile('[\u4e00-\u9fa5]|[\u3400-\u4db5]')
NUM_ENG_REGEX = re.compile('[a-zA-Z0-9?？]')

def make_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    

def get_all_files(root):
    file_names = os.listdir(root)
    file_ob_list = []
    
    # macos folder files
    for file_name in file_names:
        if file_name != ".DS_Store":
            file_ob_list.append(file_name)
   
    return file_ob_list


def cut_sentences(para):
    para = re.sub(r"([。！；？\!\?\.．…;])\1+", r"\1", para)
    para = re.sub('([。！；？\!\?\.．…;])([^”’」』])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’」』])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’」』])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！；？\!\?\.．…;][”’」』])([^，。！；？\!\?\.．…;])', r'\1\n\2', para)
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    sentences = para.split("\n")
    sentences = [sent for sent in sentences if len(sent.strip()) > 0]

    return sentences


def judge_chinese(line: str):
    c_count = 0
    e_count = 0 
    for i in line:
        if CHINESE_REGEX.match(i) != None:
            c_count += 1
        elif NUM_ENG_REGEX.match(i) != None:
            e_count += 1
    
    if c_count < e_count * 10:
        return False
    else:
        return True
    
    
def process_all_zh_files(root, target_root, target_file): 
    train_f = open(root, "r", encoding='utf-8-sig',errors='ignore')
    output = open(target_root + target_file, "w+", encoding='utf-8-sig', errors='ignore')
   
    for item in tqdm(train_f.readlines()):
        text = json.loads(item[:-1])['content'].strip()
        if not judge_chinese(text):
            continue
        text_list = cut_sentences(text)
        for sentence in text_list:
            res = filter_sentences(sentence).strip()
            if len(res) > 0:
                for i in jieba.lcut(res):
                    output.write(i)
                    output.write(' ')
                output.write('\n')
    output.close()
    train_f.close()
    

def process_all_news_files(root, target_root, target_file):  
    train_f = open(root, "r", encoding='utf-8',errors='ignore')
    output = open(target_root + target_file, "w+", encoding='utf-8', errors='ignore')
    
    for text in tqdm(train_f.readlines()):
        if not judge_chinese(text):
            continue
        text_list = cut_sentences(text)
        for sentence in text_list:
            res = filter_sentences(sentence).strip()
            if len(res) > 0:
                for i in jieba.lcut(res):
                    output.write(i)
                    output.write(' ')
                output.write('\n')
    output.close()
    train_f.close()
        
            
def process_all_nlpcc_files(root, target_root, target_file):
    # make_dir(target_root)   
    train_f = open(root, "r", encoding='utf-8',errors='ignore')
    output = open(target_root + target_file, "w+", encoding='utf-8', errors='ignore')
    
    for t in tqdm(train_f.readlines()):
        text = json.loads(t[:-1])
        text = text['summarization'] + "。" + text['article']
        
        if not judge_chinese(text):
            continue
        text_list = cut_sentences(text)
        for sentence in text_list:
            res = filter_sentences(sentence).strip()
            if len(res) > 0:
                for i in jieba.lcut(res):
                    output.write(i)
                    output.write(' ')
                output.write('\n')
    output.close()
    train_f.close()     

    
def merge_files(root, target, convert):
    
    converter = opencc.OpenCC('s2t.json')
    file_names = get_all_files(root)
    output = open(target, "w+", encoding='utf-8', errors='ignore')
    for file_name in file_names:
        f = open(root + file_name, "r", encoding='utf-8',errors='ignore')
        for line in tqdm(f.readlines(), desc="merge lines in a file"):
            if convert:
                output.write(converter.convert(line))
            else:
                output.write(line)
        f.close()
    output.close()

