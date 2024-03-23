# -*- coding: utf-8 -*-
import re
import sys,os
basedir = os.path.dirname(__file__)
parent_dir = os.path.dirname(basedir)

project_dir=basedir 
# 遍历所有父节点目录 如果存在readme.md文件 就返回那个目录
while True:
    if os.path.exists(os.path.join(project_dir, 'readme.md')):
        break
    project_dir = os.path.dirname(project_dir)
    if project_dir==os.path.dirname(project_dir):
        raise ValueError('未找到项目根目录')


sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(os.path.dirname(os.path.dirname(parent_dir)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))))

os.chdir(basedir)

print('basedir-------------->',basedir)
sys.path.append(basedir)


from concurrent.futures import ThreadPoolExecutor
import time

import json
import re
from DrissionPage import ChromiumOptions,SessionPage,ChromiumPage
from loguru import logger


user_data_dir=f'{project_dir}/user_data/douyin/'
os.makedirs(user_data_dir,exist_ok=True)
co=ChromiumOptions().set_user_data_path(user_data_dir)
# co=ChromiumOptions().headless().set_user_data_path(user_data_dir)
page = ChromiumPage(co)
page.get('https://creator.douyin.com/creator-micro/content/upload')
page.wait.doc_loaded()

from loguru import logger
from redisbloom.client import Client
from pymongo import MongoClient
import redis 
#mongodb://root:1213wzwz@139.196.158.152:27017/admin

table_name='douyin_push'
table_detail=f'{table_name}_detail'

client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

db = client.zhiqiang_hot
table=db[table_name]
from utils.utils import *

def process(data):
    _id=data['_id']
    ok_mp4=data['ok_mp4']
    index_img=data['index_img']
    index_id=data['index_id']


    try:
        btn_ele=page.ele('@name=upload-btn',timeout=10)
        page.set.upload_files(ok_mp4)
        btn_ele.click()
        page.wait.upload_paths_inputted()

        table.update_one({'_id':_id},{'$set':{'step':ok_status,'index_id':index_id}})
        logger.success(index_id)
    except Exception as e:
        logger.error(f'{index_id}    {e }')



if __name__ == '__main__':
    from_status=6
    temp_status=7
    ok_status=8
    other_status=18
    error_status=18

    max_work = 1
    executor = ThreadPoolExecutor(max_work)

    table.update_many({'step':temp_status},{'$set':{'step':from_status}})
    table.update_many({'step':error_status},{'$set':{'step':from_status}})
    index_id=0
    while 1:
        if executor._work_queue.qsize()  > max_work:
            time.sleep(10)
            continue
        
        data=table.find_one_and_update(
                                {'step':from_status,'index_id':index_id},
                                {'$set':{'step':temp_status}}
                                    )
        index_id+=1
        if not(data):
            logger.error(f'队列空----> {index_id}.mp4 还没有下载')
            time.sleep(1)
            continue

        _id=data['_id']
        executor.submit(process, data)

    executor.shutdown(wait=True)

    logger.info(' control c  ----> ')
    logger.info('<----  退出线程池  ----> ')
    os._exit(0)
