from tqdm import tqdm
import os


def get_all_files(root):
    file_names = os.listdir(root)
    file_ob_list = []
    
    # mac特殊文件
    for file_name in file_names:
        if file_name != ".DS_Store":
            file_ob_list.append(file_name)
   
    return file_ob_list


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