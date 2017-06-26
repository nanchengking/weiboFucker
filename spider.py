#coding=utf-8
import csv
import wordcloud
import jieba
import requests
import time
import codecs


def cleanring(text):
    '''
    clean text
    '''
    return text

def fetch_weibo():
    cookies=read_cookie()
    for i in range(1, 102):
        print("fetch number: %s"%i)
        api = "http://m.weibo.cn/index/my?format=cards&page=%s"%i
        response = requests.get(url=api, cookies=cookies).json()
        if not response:
            print("no response!!!")
            break
        data = response[0]
        groups = data.get("card_group") or []
        for group in groups:
            text = group.get("mblog").get("text")
            text = text.encode("utf-8")
            text = cleanring(text).strip()
            yield text

def read_cookie():
    '''
    读取cookei
    '''
    cookie=open("cookie.txt")
    cookie=cookie.read()
    cookie_map={}
    for i in cookie.split(';'):
        arr=i.split("=")
        cookie_map[arr[0].strip()]=arr[1].strip()
    return cookie_map
def write_csv(texts):
    '''
    保存数据
    '''
    with codecs.open('weibo.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["text"])
        writer.writeheader()
        for text in texts:
            writer.writerow({"text": text})


if __name__ =="__main__":
    print("start")
    write_csv(fetch_weibo())



def read_csv():
    with codecs.open('weibo.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row['text']



def word_segment(texts):
    '''
    分词处理
    '''
    jieba.analyse.set_stop_words("stopwords.txt")
    for text in texts:
        tags = jieba.analyse.extract_tags(text, topK=20)
        yield " ".join(tags)

def generate_img(texts):
    data = " ".join(text for text in texts)
    mask_img = imread('./heart-mask.jpg', flatten=True)
    wordcloud = WordCloud(
        font_path='msyh.ttc',
        background_color='white',
        mask=mask_img
    ).generate(data)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('./heart.jpg', dpi=600)

