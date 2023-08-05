'''
Author: your name
Date: 2021-07-22 18:30:20
LastEditTime: 2021-07-22 20:49:57
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \get_ris\get_ris\download_pdf.py
'''
from os import path
import os
import re
import requests
class IEEEDownloader:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}
    def get_download_url(self,session,ar_num):
        """ Start a session and acquire the url according to ar_number

        Args:
            session ([type]): [description]
            ar_num ([type]): [description]

        Returns:
            None: None
        """
        base_url = 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber='+str(ar_num)
        r = session.get(base_url,stream = True).content
        # 在接收到的html中获取pdf的下载位置
        url = re.findall('iframe src="(.*?)" frameborder.*?',str(r))[0]
        return url

    def download_url(self,url,path,out_file):
        """Downloading pdf according to url

        Args:
            url (str): url of pdf file
            path (str): download path
            out_file (str): file location
        """
        r = requests.get(url,stream = True)
        with open(path+out_file,'wb') as f:
            f.write(r.content)

    def download_pdf(self,path,ar_number,file_name):
        url = self.get_download_url(session=self.session,ar_num=ar_number)
        self.download_url(url=url,path = path,out_file=f'{file_name}.pdf')
        return path+file_name+'.pdf'

if __name__ == '__main__':
    down = IEEEDownloader()
    ar_number = '8008942'
    down.download_pdf(ar_number=ar_number)
    
    