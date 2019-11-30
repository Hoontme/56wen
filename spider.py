# this is a python script for web's txt
import requests
import re
from bs4 import BeautifulSoup
import os 
headers_data = {"Referer": "http://www.56wen.com/zhuanji/"
,"Upgrade-Insecure-Requests": "1"
,"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }

#home_url is the zhuanji's homepage
home_url = "http://www.56wen.com"
#然后我们找到\传记\系列的第一本书的地址
#album_name = /zhuanji
def albums(album_name):
    global home_url
    global header_data
    zhuanji_url = home_url + album_name  
    try:
        r =requests.get(zhuanji_url,headers = headers_data)
        r.raise_for_status()
    except:
        print("requests.get {} false".format(zhuanji_url))
    #analyse the first page of zhuanji with bs4 ,get the first book,and maybe all the book with a loop later.
    
    #soup = Beautifulsoup(r.text)
    contentss=re.findall("a href=\"(/txt/[0-9]+.html)",r.text)
    #获得传记第一页20本书的首页网址
    contents=list(set(contentss[0:40]))
    content=["www.56wen.com"]*len(contents)+contents
    #for i in range(len(content)):
     #   content[i]="www.56wen.com"+content[i]
    return content
#从第一本书跳转到阅读，然后批量下载本书所有页面，从album函数引入content到book_url
def download_book(book_url):
    #bookurl是在main函数中补全以后的网址
    global headers_data
    r=requests.get(book_url,headers=headers_data)
    #通过下面的命令获取全书的章节链接
    #content=re.findall("li><a href=\"http://www.56wen.com/book(/[0-9]+/[0-9]+.html)",r.text)
    chapter=re.find("href=\"(http://www.56wen.com/chapter.+html)",r.text)
    r=requests.get(chapter,headers=headers_data)
    chapter_book=re.findall("a href=\"(/book.+html)",r.text)
    #将所有章节的网址和开头合并
    init_url=["http://www.56wen.com"]*len(chapter_book)+chapter_book
    return init_url

#根据每一页的内容下载引入download_book
def down_page(page_url):
    book_text=[]
    for i in page_url:
        r=requests.get(i,headers=headers_data)
        soup = BeautifulSoup(r.text,"html.parser")
        book_text += soup.find_all("div",id="J_article_con")
    
    title = soup.title.string
    if os.exists.path("D:/360Wifi/zhuanji"):
        continue
    else:
        os.mkdir("D:/360Wifi/zhuanji")
        
    try:
        with open("D:/360Wifi/zhuanji/{}.txt".format(title),"a") as f:
            for i in book_text:
                f.write(i)
            f.close()
                        
    else:
        print("down_page wrong")
if __name__=="__main__":
    s=albums("/zhuanji")
    ss=download_book(s)
    sss=down_page(ss)

