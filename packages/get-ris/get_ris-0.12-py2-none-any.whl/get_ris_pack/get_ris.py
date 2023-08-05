'''
Author: your name
Date: 2021-07-06 09:22:09
LastEditTime: 2021-07-22 21:42:01
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \get_ris\get_ris\get_ris.py
'''
#-*- encoding: UTF-8 -*-
import requests
import re
import os
import sys
import json
import logging

from get_ris_pack.download_pdf import IEEEDownloader
from get_ris_pack.get_info_by_id import get_info_by_id
from get_ris_pack.read_clipboard import getText
def get_download_path():
    cfg_path = os.path.split(os.path.realpath(__file__))[0]+'\\config.txt'
    if(os.path.isfile(cfg_path)):
        with open(cfg_path,'r') as f:
            path = f.readlines()[0]
        return path
    return ''

def set_download_path(path):
    cfg_path = os.path.split(os.path.realpath(__file__))[0]+'\\config.txt'
    with open(cfg_path,'w') as f:
        f.write(path)
        
def start():
    pdf_path = get_download_path()
    if(pdf_path== ''):
        return
    url = getText()
    try:
        id = re.findall("(\d{6,})",url)[0]
    except IndexError:
        print("[ERROR] Not valid url")
        return
    print('[INFO] Downloading RIS ...')
    try:
        info = get_info_by_id(id)
        with open(f'{pdf_path}temp.ris','w') as f:
            f.write(str(info))
        print(f'[INFO] RIS finished')
        os.system(f'{pdf_path}temp.ris')
        
    except Exception as e:
        print(e)

def start_pdf():
    pdf_path = get_download_path()
    if(pdf_path== ''):
        print("no path")
        return
    down = IEEEDownloader()
    url = getText()
    try:
        id = re.findall("(\d{6,})",url)[0]
    except IndexError:
        print("[ERROR] Not valid url")
    try:
        print('[INFO] Downloading RIS ...')
        info = get_info_by_id(id)
        print('[INFO] Downloading PDF, this may take several minutes ...')
        file_path = down.download_pdf(pdf_path,id,info.title)
        print(f'[INFO] Finished downloading to {file_path}')
        
        with open(f'{pdf_path}temp.ris','w') as f:
            f.write(str(info))
            f.write(f'%> {file_path}')
        print(f'[INFO] RIS finished')
        os.system(f'{pdf_path}temp.ris')
        
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    start()
    
