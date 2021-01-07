import re
import html
import urllib
import w3lib.html

CHINESE_REGEX = re.compile('[\u4e00-\u9fa5]')
NUM_ENG_REGEX = re.compile('[a-zA-Z0-9]')
URL_REGEX = re.compile(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                re.IGNORECASE)
EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
QQ_REGEX = re.compile(r"QQ群?:?：?[1-9]\d{4,10}", re.IGNORECASE)
allpuncs = re.compile(r"[，，\_《。》？；：‘’＂“”【「】」、·！@￥…（\(）\)—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+▼●■◆◇]")


def filter_sentences(text: str):

    text = "".join(text.split())
    
    # delete redundant
    text = re.sub("（一.+?）|（二.+?）|（三.+?）|（四.+?）|（五.+?）|（六.+?）|（七.+?）|（八.+?）|（九.+?）|（十.+?）|一、|二、|三、|四、|五、|六、|七、|八、|九、|十、|",'',text)
    
    # delete brackets
    text = re.sub("（.+?）",'',text)
    text = re.sub("\(.+?\)",'',text)
    text = re.sub("【.+?】",'',text)
    text = re.sub("「.+?」",'',text)
    text = re.sub("［.+?］",'',text)
    text = re.sub("〔.+?〕",'',text)
    text = re.sub("\[.+?\]",'',text)
    text = re.sub("\<.+?\>",'',text)
    
    # delete email links, emojis and other Weibo things
    text = html.unescape(text)
    text = urllib.parse.quote(text)
    text = w3lib.html.remove_tags(text)
    text = re.sub(URL_REGEX, "", text)
    text = urllib.parse.unquote(text)
    text = re.sub(EMAIL_REGEX, "", text)
    text = re.sub(QQ_REGEX, "", text)
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)
    text = re.sub(r"\[\S+\]", "", text)
    text = re.sub(r"#\S+#", "", text)
    text = re.sub(r"\s+", " ", text)
    
    # English punctuations to Chinese
    text = re.sub(",","，", text)
    text = re.sub(":","：", text)
    text = re.sub("：+，", "，", text)
    text = re.sub("、+，", "，", text)
    text = re.sub("、+：", "：", text)
    text = re.sub("，+：", "：", text)
    text = re.sub("：+、", "：", text)
    text = re.sub("，+、", "，", text)
    text = re.sub(r"，+", '，', text)
    text = re.sub(r"、+", '、', text)
    text = re.sub(r"：+", '：', text)
    text = re.sub(r"？+", '？', text)
    text = re.sub(r"！+", '！', text)
    text = re.sub(r"^，", '', text)
    text = re.sub(r"，$", '', text)
    
    # delete single words
    if len(text) == 1:
        return ""
   
    return text