
# coding:utf-8
import re
import json
import time
import random
import sys

from pathlib import Path
from urllib import parse
from urllib import error
from urllib import request
from http.client import IncompleteRead
from socket import timeout as socket_timeout
from bs4 import BeautifulSoup

def create_dir(name):
    directory = Path(name)
    if not directory.exists():
        directory.mkdir()
    return directory

def get_query_string(data):
    return parse.urlencode(data)

def get_article_urls(req,timeout=10):
    with request.urlopen(req,timeout=timeout) as res:
        d=json.loads(res.read().decode()).get('data')
        if d is None:
            print('数据全部请求完毕')
            return
        urls=[article.get('article_url') for article in d if article.get('article_url')]
        return urls

def get_photo_urls(req,timeout=10):
    with request.urlopen(req,timeout=timeout) as res:
        soup=BeautifulSoup(res.read().decode(errors="ignore"),'html.parser')
        article_main=soup.find('div',id='article-main')
        if not article_main:
            print('无法定位到文章主体')
            return
        heading=article_main.h1.string
        if '街拍' not in heading:
            print('这不是街拍的文章') 
            return
        img_list=(img.get('src') for img in article_main.find_all('img') if img.get('src'))   
        return heading,img_list

def save_photo(photo_url,save_dir,timeout=10):
    photo_name=photo_url.rsplit('/',1)[-1]+'.jpg'
    save_path=save_dir/photo_name
    with request.urlopen(photo_url,timeout=timeout) as res,save_path.open('wb') as f:
        f.write(res.read())
        print('已下载图片：{dir_name}/{photo_name},请求的URL为：{url}'
                .format(dir_name=dir_name,photo_name=photo_name,url=a_url))


if __name__ == '__main__':
    ongoing=True
    offset=0
    root_dir=create_dir('./examples')
    request_headers = {
        'Referer': 'http://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }

    while ongoing:
        query_data = {
            'offset': offset,
            'format': 'json',
            'keyword': '街拍',
            'autoload': 'true',
            'count': 20,  
            '_': 'cur_tab=1'
        }
        query_url='http://www.toutiao.com/search_content/' + '?' + get_query_string(query_data)
        article_req=request.Request(query_url,headers=request_headers)
        artticle_urls=get_article_urls(article_req)
        if artticle_urls is None:
            break
        for a_url in artticle_urls:
            try:
                photo_req=request.Request(a_url,headers=request_headers)
                photo_urls=get_photo_urls(photo_req)
                if photo_urls is None:
                    continue
                article_heading,photo_urls=photo_urls
                dir_name=re.sub(r'[\\/?<>*|:"]',' ',article_heading)
                download_dir=create_dir(root_dir/dir_name)
                for p_urls in photo_urls:
                    try:
                        save_photo(p_urls,save_dir=download_dir)
                    except IncompleteRead as e:
                        print('e')
                        continue
            except socket_timeout:
                print('连接超时，休息一下')
                time.sleep(random.randint(15,25))
                continue
            except error.HTTPError:
                continue
            except KeyboardInterrupt:
                print('你已经用CTRL+C结束了程序')
                sys.exit()

        offset += 20
                  


    
















