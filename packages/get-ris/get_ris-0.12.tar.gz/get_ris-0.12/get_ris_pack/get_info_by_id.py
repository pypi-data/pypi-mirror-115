import requests
import os
import json
from get_ris_pack.article import Article
import re
import urllib3


session = requests.Session()
session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}

def get_download_url(ar_num):
    base_url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber='+str(ar_num)
    r = session.get(base_url,stream = True).content
    # 在接收到的html中获取pdf的下载位置
    url = re.findall('iframe src="(.*?)" frameborder.*?',str(r))[0]
    return url

def download_url(url,path,out_file):
    r = requests.get(url,stream = True)
    with open(path+out_file,'wb') as f:
        f.write(r.content)

def get_info_by_id(ar_number):
    urllib3.disable_warnings()
    url = f'https://ieeexploreapi.ieee.org/api/v1/search/articles?article_number={ar_number}&apikey=ab75bvpx4e7f6yp4setb6y24'
    content = session.get(url,stream = True,verify=False).content
    data = json.loads(content.decode())

    if(data['total_records'] is 0):
        print('No file')
        return
    elif(data['total_records']>1):
        print('File more than one, get the first one')
    article = data['articles'][0]

    _title = article['title']
    _authors_raw = article['authors']['authors']
    _authors = []
    for author in _authors_raw:
        _authors.append(author['full_name'])
    _abstract = article['abstract']
    _type = article['content_type']
    _publisher = article['publication_title']
    _year = article['publication_year']

    return Article(title=_title,authors=_authors,year=_year,_type=_type,publisher=_publisher,abstract=_abstract)

if __name__ =='__main__':
    info = get_info_by_id('9235687')
    with open('.\\test.ris','w') as f:
        f.write(str(info))