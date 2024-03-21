# -*- coding: utf-8 -*-
import re
import signal
import sys,os
import time
from urllib.parse import urlparse

from loguru import logger
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))

os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)




from utils.utils import *

from test import m3u8_to_mp4

import requests
headers = {
    'authority': 'www.xiazaitool.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://xiazaitool.com',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
}

# 请求网络第三方接口
def get_play_url(uid_aid):
    data = {
        'platform': 'kuaishou',
        'url': f'https://www.kuaishou.com/short-video/{uid_aid}',
    }

    response = requests.post('https://www.xiazaitool.com/video/parseVideoUrl', headers=headers, json=data)
    try:
        res=response.json()
    except Exception as e:
        print(response.text)
        raise ValueError('111111')
        
    return res

# 自己实现一套逻辑就是快手的api嘛

import json
import re
from DrissionPage import ChromiumOptions,SessionPage,ChromiumPage
from loguru import logger
co=ChromiumOptions()
# co=ChromiumOptions().headless()
page = ChromiumPage(co)


def get_play_url_zq(uid):
    url=f'https://www.kuaishou.com/short-video/{uid}'
   
    page.listen.start('m3u8')  # 开始监听，指定获取包含该文本的数据包
    page.get(url)  # 访问网址

    for packet in page.listen.steps(timeout=10):
        m3u8_url=packet.url
        desc=page.title
        return m3u8_url,desc
    return None,None

import os
import requests
from concurrent.futures import ThreadPoolExecutor
from m3u8 import M3U8




from redisbloom.client import Client
from pymongo import MongoClient
import redis 
#mongodb://root:1213wzwz@139.196.158.152:27017/admin

table_name='douyin_push'

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

db = client.zhiqiang_hot
table=db[table_name]


from concurrent.futures import ThreadPoolExecutor
def close(signum, frame):
    global signal_on, executor
    signal_on = False
    logger.info(f'closing spider by signal {signum}')
    active_count = executor._threads.__len__()  # 活动线程数
    queue_size = executor._work_queue.qsize()  # 工作队列大小
    logger.info(f'executor status: 活动线程数 ={active_count}, 工作队列大小={queue_size}')


signal_on = True
signal.signal(signal.SIGINT, close)
signal.signal(signal.SIGTERM, close)

"""https://v4-vod.kwaicdn.com/ksc2/qb2OvbGnKLAas1p00Ct3Bq1svQb-CqKMBk_uMTn76aOAlha7B5o4Yjt36ztbQ__66dP8NIO3CY1jjVMraUE0rw.m3u8?pkey=AAVeaxsFZqFxY_Dl082UzUQIWMsO5MEzz-NjVedQkAa5yGn4_DqGRADKg233gW-rYELmRBwaJ5qzztJHsUGNobvSGhl724_Jx5f4MvJbO3FT9rWgE_oeTEaKGGManFyIi_4&ss=vp
"""

"""
https://v4-vod.kwaicdn.com/ksc2/QvJbDvdZSlKGEUDDmmW-fNtfJV4gLZz29nGY827RQTZ6oHVI7P80YkJqEpoqlaTeavcC0idTj-BJVFzP3QgBJA.m3u8?pkey=AAUBK3uhc7TNDYM34DIGcfhJECn-2w9eP-A_ymOme_v_MKleb0Mopu6uPU9lPaQQ_8_27HDdq3BneaMrXhrhlmEM8-lTnGVz0ho_FzWtt-1bNVhujmHKQvHGfdBRTijJqrs&ss=vp

"""

"""
https://v4-vod.kwaicdn.com/ksc2/QvJbDvdZSlKGEUDDmmW-fNtfJV4gLZz29nGY827RQTZ6oHVI7P80YkJqEpoqlaTeavcC0idTj-BJVFzP3QgBJA.00003.ts?pkey=AAUBK3uhc7TNDYM34DIGcfhJECn-2w9eP-A_ymOme_v_MKleb0Mopu6uPU9lPaQQ_8_27HDdq3BneaMrXhrhlmEM8-lTnGVz0ho_FzWtt-1bNVhujmHKQvHGfdBRTijJqrs

00152
"""

from urllib.parse import urljoin

def process(data):
    _id=data['_id']
    clientCacheKey=data['clientCacheKey']
    ok_mp4=data['ok_mp4']

    m3u8_file=f'C:/projects/py_win/assert/龙珠/{_id}/m3u8/'
    ts_dir=f'C:/projects/py_win/assert/龙珠/{_id}/ts/'
    ts_file_list=[]
    os.makedirs(m3u8_file,exist_ok=True)
    try:
        # 调用浏览器下载m3u8文件 统一交给它解析ts 然后还用它下载ts到一个目录下面
        m3u8_url,desc=get_play_url_zq(clientCacheKey)
        flag,m3u8_local_finename=page.download(m3u8_url, m3u8_file)
        if not(flag):
            raise ValueError('m2u8失败')
        
        with open(m3u8_local_finename,'r',encoding='utf-8') as f:
            for row in f:
                if 'ts?' not in row :
                    continue
                ts_url=urljoin(m3u8_url,row.strip())
                flag,ts_local_name=page.download(ts_url, ts_dir,show_msg=False)
                if not(flag):
                    raise ValueError('ts下载失败')
        
        merge_to_mp4(ok_mp4, ts_dir, delete=True)


        table.update_one({'_id':_id},{'$set':{'step':ok_status,}})
        logger.success(f"https://www.kuaishou.com/short-video/{clientCacheKey}")
    except Exception as e:
        logger.error(f"https://www.kuaishou.com/short-video/{clientCacheKey}   {e}")
        table.update_one({'_id':_id},{'$set':{'step':error_status,}})




if __name__ == '__main__':
    from_status=2
    temp_status=3
    ok_status=4
    error_status=14
    other_status=114

    max_work = 1
    executor = ThreadPoolExecutor(max_work)

    table.update_many({'step':temp_status},{'$set':{'step':from_status}})

    while 1:
        if executor._work_queue.qsize()  > max_work:
            time.sleep(10)
            continue

        data=table.find_one_and_update({'step':from_status},{'$set':{'step':temp_status}})

        if not(data):
            logger.error(f'队列空')
            time.sleep(77)
            continue

        _id=data['_id']
        clientCacheKey=data['clientCacheKey']

        executor.submit(process, data)

    executor.shutdown(wait=True)

    logger.info(' control c  ----> ')
    logger.info('<----  退出线程池  ----> ')
    os._exit(0)



    

"""

 86437888
167839890

"""