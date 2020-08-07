import os,re
import requests
from urllib.request import quote


CONVERTDIR = "../../_site/"
YEAR="2020"

BLOG_URL="https://jueee.github.io/"
BAIDU_URL="http://data.zz.baidu.com/urls?site=https://jueee.github.io&token=CKhNUxDRh21xsFP3"

def getBlogAddress():
    blogs = []
    for root, dirs, files in os.walk(CONVERTDIR+YEAR):
        for f in files:
            filename = os.path.join(root, f)
            url = filename.replace(CONVERTDIR,BLOG_URL).replace("\\","/").replace("index.html","")
            print(url)
            url = quote(url, safe=";/?:@&=+$,", encoding="utf-8")
            print(url)
            blogs.append(url)
    return blogs

def getPostRequest(data):
    response = requests.post(BAIDU_URL, data="\n".join(data))
    content = response.text.encode('gbk','ignore').decode('gbk')
    print(content)

if __name__ == '__main__':
    blogs = getBlogAddress()   
    getPostRequest(blogs)
