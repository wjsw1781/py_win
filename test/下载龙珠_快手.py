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

    for packet in page.listen.steps():
        m3u8_url=packet.url
        desc=page.title
        return m3u8_url,desc
    return None,None

import os
import requests
from concurrent.futures import ThreadPoolExecutor
from m3u8 import M3U8

def download_ts(url, output_dir):
    """
    下载并保存一个 TS 文件
    
    :param url: TS 文件的 URL
    :param output_dir: 要保存的目录路径
    """
    filename = os.path.basename(url)
    output_path = os.path.join(output_dir, filename)
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f"{filename} 已下载")

def download_m3u8(url, output_dir):
    """
    下载并保存 M3U8 文件以及其中的所有 TS 文件
    
    :param url: M3U8 文件的 URL
    :param output_dir: 要保存的目录路径
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    m3u8_obj = M3U8.load(url)
    ts_urls = m3u8_obj.segments.uris
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for ts_url in ts_urls:
            futures.append(executor.submit(download_ts, ts_url, output_dir))
        for future in futures:
            future.result()
    print("所有 TS 文件已下载完毕")



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


def process(data):
    _id=data['_id']
    clientCacheKey=data['clientCacheKey']

    try:
        # info=get_play_url(clientCacheKey)
        m3u8_url,desc=get_play_url_zq(clientCacheKey)
        name=get_safe_title(desc).replace('快手','抖音')+'.mp4'
        out=os.path.abspath(f'../assert/龙珠/{name}')
        m3u8_to_mp4(m3u8_url,out)

        # videoURL=info['voideDeatilVoList'][0]['url']
        # title=info['voideDeatilVoList'][0]['title']

        # desc=get_safe_title(title).replace('快手','抖音')
        # out=os.path.abspath(f'../assert/龙珠/{desc}.mp4')

        # download_flag=download_url_big_file_sync(videoURL,out)

        # if not(download_flag):
        #     raise Exception('下载失败')

        table.update_one({'_id':_id},{'$set':{'step':ok_status,'videoURL':m3u8_url,'ok_mp4':out}})
        logger.success(f"https://www.kuaishou.com/short-video/{clientCacheKey}")
    except Exception as e:
        logger.error(f"https://www.kuaishou.com/short-video/{clientCacheKey}   {e}")




if __name__ == '__main__':
    from_status=0
    temp_status=1
    ok_status=2
    other_status=3
    error_status=112

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


        if  data['clientCacheKey'] in ['3xzjip425py83gq','3xkbbb2ene9bzhg_ccc']:
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