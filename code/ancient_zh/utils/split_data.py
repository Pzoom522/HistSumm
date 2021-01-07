#!/usr/bin/env python
# coding: utf-8

import os
import tqdm
import shutil
import pandas as pd
import re
from utils import helper
from utils import regu

mark_rate = 0.1
chinese_regex = re.compile('[\u4e00-\u9fa5]|[\u3400-\u4db5]')
TARGET_CHARS = ['，', '。', '、', '：', '“', '”', '；', '○', '？']

def get_files_info(files_path):
    file_info = []
    file_list = helper.get_all_files(files_path)
    for file in tqdm.tqdm(file_list, desc="generating file info"):
        info = {
            'token_count': 0,
            'chinese_count': 0,
            'mark_count': 0,
            'mark_list': []
        }
        lines = open(files_path + file, 'r', encoding='utf-8-sig').read().splitlines()
        for line in lines:
            line = line.strip()
            for char in line:
                if helper.chinese_regex.match(char):
                    info['chinese_count'] += 1
                elif char in TARGET_CHARS:
                    info['mark_count'] += 1
                    info['mark_list'].append(char)

        info['token_count'] = info['chinese_count'] + info['mark_count']
        info['mark_list'] = ' '.join(set(info['mark_list']))
        info['mark_rate'] = info['mark_count'] / info['token_count']
        info['file'] = file.replace(files_path, '')
        file_info.append(info)
    df = pd.DataFrame(file_info)
    df.to_csv('file_info.csv')
    return df


# Analyse punctuation status and relocate files into "marked" and "unmarked" folders
def split_marked_unmarked_files(original_path: str, target_path: str):
    helper.make_dir(target_path)
    marked_path = target_path + "marked/"
    unmarked_path = target_path + "unmarked/"
    helper.make_dir(marked_path)
    helper.make_dir(unmarked_path)
    df = get_files_info(original_path)

    marked_df = df[df['mark_rate'] >= mark_rate]
    unmarked_df = df[df['mark_rate'] < mark_rate]
    columns = list(df.columns)

    def copy_files(t_df: pd.DataFrame, copy_to_path: str):
        for file in tqdm.tqdm(t_df.values, desc='copying files to {}'.format(copy_to_path)):
            file_name = file[columns.index('file')]
            shutil.copy(os.path.join(original_path + file_name), copy_to_path)

    copy_files(marked_df, marked_path)
    copy_files(unmarked_df, unmarked_path)

