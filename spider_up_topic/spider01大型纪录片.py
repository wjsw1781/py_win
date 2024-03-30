# -*- coding: utf-8 -*-
import datetime
import re
import sys,os

from pymongo import MongoClient
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


from utils import bilibili
from item_status import Vidoe_Item_Status
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot
from utils.utils import *


# 总共操纵两个表 一个所有发布这种视频的up主 id  一个是所有视频id
table_one=db['daxingjilupian_ups']
table_two=db['daxingjilupian_videos']

item={
    'uid':498421499,
    'key':498421499,
    'up_name':"我是李四儿",
    '_id':md5(498421499),
}
table_one.update_one({'_id':item['_id']},{'$set':item},upsert=True)

# 入库 下载  抽帧  质检  投稿

def into_db():
    add_count=0
    uids =list(table_one.find())

    for recorder in uids:
        uid=recorder['uid']
        uid=int(uid)
        all_video = bilibili.get_all_videos_sync(uid, 3)

        good_video = list(filter(lambda x: x['play'] > 10000, all_video))

        for video in good_video:
            safe_title = get_safe_title(video['title'])
            bvid = video['bvid']
            aid = video['aid']
            item = {
                "_id":md5(bvid),
                **video,
                "shuiyin_bili":0,
                "shijianzhou_delete_length":0,
                "new_shuiyin_bili":0,
                "new_shijianzhou_delete_length":0,
                "safe_title":safe_title,
            }
            table_two.update_one({'_id':item['_id']},{'$set':item},upsert=True)
            add_count+=1
    
    return add_count
    pass

def download_video(item):
    pass

def get_4_frame_pics(item):
    pass

def check_video(item):
    pass

def upload_video(item):
    pass


curent_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if __name__ == '__main__':
    try:
        add_count=into_db()
        if add_count==0:
            raise ValueError(f"没有成功爬取到视频信息 by_uid 结果为 add_count  {add_count}")
        logger.success(f"{curent_time}  爬取陈工  {add_count} 条入库")
    except Exception as e:
        tell_to_wx(str(e))
    




            # local_name = os.path.abspath(f'./assert/大型纪录片/{safe_title}')
            # pic_index = f"{local_name}/index.jpg"
            # pic_index_url = video['pic']
            # video_mp4_name = f"{local_name}/video.mp4"
            # video_mp4_namegood = video_mp4_name + "good.mp4"
            # frame_pics=[]
            # # 四张抽帧图片截图
            # for ii in range(4):
            #     frame_ii = f"{local_name}/frame_{ii}.jpg"
            #     frame_pics.append(frame_ii)

            # os.makedirs(local_name, exist_ok=True)

            # if os.path.exists(video_mp4_name):
            #     if os.path.exists(video_mp4_namegood):
            #         continue

            # import requests
            # with open(pic_index, 'wb') as ff:
            #     ff.write(requests.get(pic_index_url).content)

            # flag = bilibili.download_video_sync(bvid=bvid, aid=aid, filename=video_mp4_name)
            # if not (flag):
            #     logger.error(f"下载失败---->  {video_mp4_name}")
            #     continue
            # logger.success(f"下载陈工---->  {video_mp4_name}")
