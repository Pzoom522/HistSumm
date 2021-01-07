import re

chinese_regex = re.compile('[\u4e00-\u9fa5]')

TARGET_CHARS = ['，', '。', '】', '【', '、', '：', '“', '”', '；', '》', '《', ')', '(', '?', '!']
ac_token = re.compile("[^，：、\u4e00-\u9fa5]")
known_token = re.compile("[^。，；？！\u4e00-\u9fa5”’」』：、]")
end_token = ['。','；','？','！','．','?','!','.','…']
weird = re.compile("[○]")
flag1 = False
flag2 = False

# Filter book names and song lyrics
def filter_special(line):
    s = line.strip()
    global flag2
    
    # filter lyrics, medical ingredients in 《武编》 and locations in《江南经略》
    if re.search("火箭头白火|解箭头药名|杂术|苏州府土贼要害|沿海墪塘考|濠周于城|柘林堡城池考|青邨所城池考|下邾险要说", s) != None:
        flag2 = True
    elif re.search("达达蒜|盐麸子|汉髙帝时黥布反|松江府总论|西仓堡守御论|以船易马议|柘林堡兵防考|青邨所兵防考|镇江府守城官兵考", s) != None:
        flag2 = False
        return ""
    if flag2 is True:
        return ""
    
    # Filter sentences
    s = re.sub("太宗文皇帝实录.*",'',s)
    s = re.sub("明卷之.*",'',s)
    s = re.sub("太宗至孝文皇帝实录卷.*",'',s)
    s = re.sub("明太宗孝文皇帝实录卷.*",'',s)
    s = re.sub("大明，太宗孝文皇帝实录卷.*",'',s)
    s = re.sub("武编后集卷.*|武编前集卷.*|<子部，,兵家类，,武编>.*",'',s)
    s = re.sub("江南经畧卷.*",'',s)
    s = re.sub("钦定四库全书",'',s)
    s = re.sub("^甲子|乙丑|丙寅|丁卯|戊辰|己巳|庚午|辛未|壬申|癸酉|甲戌|乙亥|丙子|丁丑|戊寅|己卯|庚辰|辛己|壬午|癸未|甲申|乙酉|丙戌|丁亥|戊子|己丑|庚寅|辛卯|壬辰|癸巳|甲午|乙未|丙申|丁酉|戊戌|己亥|庚子|辛丑|壬寅|癸卯|甲辰|乙巳|丙午|丁未|戊申|己酉|庚戌|辛亥|壬子|癸丑|甲寅|乙卯|丙辰|丁巳|戊午|己未|庚申|辛酉|壬戌|癸亥$",'',s)
    s = re.sub("^卷之.*|^卷.*|^大明，卷.*",'',s)
    s = re.sub(".*?月朔$|^辛巳$",'',s)
    s = re.sub("锍，釒|锍，，釒",'',s)
    s = re.sub("^大明，$|^明$",'',s)
    s = re.sub("江西提学佥事，.*",'',s)
    s = re.sub("江西按察司佥事，.*",'',s)
    s = re.sub("^.*墓志铭$|^.*墓志$|^.*墓志，$",'',s)
    
    return s


def filter_marked_sentences(l: str):
   
    line = l.strip()
    
    # delete redundant
    line = re.sub("目录|提要|序|附录|作者|版本|内容|［题解］|［原注］|［批评］｜《投笔肤谈》成书于明末，是一部颇有影响的古代军事理论著作。","",line)
    line = re.sub("^第.+?。|^第\..+?回|一。|一、|—、|—。|^第.+?回","",line)
    
    if re.search(r"[。！；？\!\?\.．…;:”’』」]$",line) is None:
        return ""

    # deal with brackets
    line = re.sub(r"\(.*?\)","",line)
    line = re.sub(r"（.*?）","",line)
    line = re.sub(r"〔一.*?〕|〔二.*?〕|〔三.*?〕|〔四.*?〕|〔五.*?〕|〔六.*?〕|〔七.*?〕|〔八.*?〕|〔九.*?〕|〔十.*?〕","",line)
    line = re.sub(r"〈.*?〉.+?则","",line)
    line = re.sub(r"〈.*?〉","",line)
    line = re.sub(r"<.*?>","",line)
    line = re.sub(r"＜.*?＞","",line)
    line = re.sub(r"\[.*?\]","",line)
    line = re.sub(r"［.*?］","",line)
    line = re.sub(r"【.*?】","",line)
    line = re.sub(r"\{.*?\}","",line)
    line = re.sub(r"｛.*?｝","",line)
    line = re.sub(r"[“‘”’『』「」]",'',line)
    
    # English punctuations to Chinese
    line = line.replace(":","：")
    line = line.replace(",","，")

    line = re.sub(ac_token,"",line)  # ac_token ，：、\u4e00-\u9fa5
    line = re.sub("，+","，",line)  # multi commas into one
    line = re.sub("^，|^、|^：","",line)  # delete punctuations at the start of a sentence
    line = re.sub("，$|、$|：$","",line)  # delete punctuations at the end of a sentence
    
    if len(line) == 1:
        return ""
    
    return line


def filter_mlmarked_sentences(l: str):
    global flag1
    line = l.strip()
    
    line = re.sub("目录|提要|序|附录|作者|版本|内容|［题解］|［原注］|［批评］|校勘记|^卷之.*","",line)
    line = re.sub("^第.+?。|^第\..+?回|一。|一、|—、|—。|^第.+?回","",line)
    
    # 《江南经略》《明实录宣宗实录》《明实录孝宗实录》are too noisy
    if re.search("夏兵宪太原王公道行|朕惟我国家|报讣音于宗室诸王", line) != None:
        flag1 = True
    elif re.search("司国计者防虑而熟|己卯成服|颁遗诏于天下", line) != None:
        flag1 = False
    if flag1 is True:
        line = re.sub("^一",'',line)
        
    # delete redundant
    if re.search("^行在翰林院", line) != None:
        return ""
            
    line = re.sub("○，","",line)
    line = re.sub("○","",line)
    
    # deal with brackets
    line = re.sub(r"\(.*?\)","",line)
    line = re.sub(r"（.*?）","",line)
    line = re.sub(r"<.*?>","",line)
    line = re.sub(r"＜.*?＞","",line)
    line = re.sub(r"\[.*?\]","",line)
    line = re.sub(r"【.*?】","",line)
    
    # English punctuations to Chinese
    line = line.replace(":","：")
    line = line.replace(",","，")
    line = line.replace("、，","，")  # to fix jiayan tagging problem
    line = line.replace("：，","，")  # to fix jiayan tagging problem
    line = re.sub(ac_token,"",line)  # ac_token ，：、\u4e00-\u9fa5

    line = filter_special(line)
    
    line = re.sub(ac_token,"",line)
    line = re.sub("，+","，",line)  # multi commas into one
    line = re.sub("^，|^、|^：","",line)  # delete punctuations at the start of a sentence
    line = re.sub("，$|、$|：$","",line)  # delete punctuations at the end of a sentence
    
    if len(line) == 1:
        return ""
    
    return line

