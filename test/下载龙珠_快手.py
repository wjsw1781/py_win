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

from redisbloom.client import Client
from pymongo import MongoClient
import redis 
#mongodb://root:1213wzwz@139.196.158.152:27017/admin

table_name='douyin_push'
table_detail=f'{table_name}_detail'

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
        info=get_play_url(clientCacheKey)
        videoURL=info['voideDeatilVoList'][0]['url']
        title=info['voideDeatilVoList'][0]['title']

        desc=get_safe_title(title).replace('快手','抖音')
        out=os.path.abspath(f'../assert/龙珠/{desc}.mp4')

        download_flag=download_url_big_file_sync(videoURL,out)

        if not(download_flag):
            raise Exception('下载失败')

        table.update_one({'_id':_id},{'$set':{'step':ok_status,'info':info,'videoURL':videoURL,'ok_mp4':out}})
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