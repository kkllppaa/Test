#coding:utf-8
from urllib import request
from bs4 import BeautifulSoup
import re
import sys






def get_links(url):
    urlList=[]
    req=request.Request(url,headers=request_headers)
    with request.urlopen(req) as res:
        soup=BeautifulSoup(res.read().decode(),'html.parser')
        links=soup.find_all('a',rel="bookmark")
        for link in links:
            urls=link['href']
            print(urls)
            urlList.append(urls)
        return urlList

def get_post(url):
    req=request.Request(url,headers=request_headers)
    with request.urlopen(req) as res:
        soup=BeautifulSoup(res.read().decode(),'html.parser')
        title=soup.find('h1',class_="entry-title").text
        content=soup.find('div',class_="entry-content").text
        time=soup.find('time',class_="entry-date published").text
    # return title,content
    # title=title.encode('utf-8')
    # content=content.encode('utf-8')
    # print(content)
    with open ('/Users/lenovo/workspace/Helloworld/src/demo/gsq/gsq.txt',"a",encoding='utf-8') as f:
    
        f.write(time+title+'\n\n')
        f.write(content+'\n\n\n\n\n\n\n\n\n\n')
        
        print('当前文章：{}已经下载完毕'.format(title))
    return



if __name__ == '__main__':  
    request_headers = {
    # 'Referer': 'http://www.gushequ.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }          
    i=1    
    for i in range(1,70):
        url="http://www.gushequ.com" + '/page/'+str(i)
        print(i)
        p_urls=get_links(url)
        for a_url in p_urls:
            try:
                posts=get_post(a_url)
            except KeyboardInterrupt:
                print('你已经用CTRL+C结束了程序')
                sys.exit()


