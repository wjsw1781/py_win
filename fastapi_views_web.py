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

# 工具函数////////////////

def time_to_seconds(time_str):
    # 将时分表示转换为秒
    minutes, seconds = map(int, time_str.split(':'))
    total_seconds = minutes * 60 + seconds
    return total_seconds

def seconds_to_time(seconds):
    # 将秒转换为时分表示
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    time_str = '{:02d}:{:02d}'.format(minutes, remaining_seconds)
    return time_str


from fast_api_views_video_editor import list_page



from fastapi import FastAPI, APIRouter, Response
from fast_api_views_video_editor.list_page import router as list_router
from fast_api_views_video_editor.detail_page import router as detail_router
from fastapi.middleware.cors import CORSMiddleware

from redisbloom.client import Client
from pymongo import MongoClient
import redis 
#mongodb://root:1213wzwz@139.196.158.152:27017/admin
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)


# 数据源
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot


def get_all_table_names():
    tables = db.list_collection_names()
    return tables

def get_page_data(table_name, page_num, page_size):
    # 获取指定表的指定页的数据
    collection = db[table_name]
    # 计算跳过的数据数量
    skip = (page_num - 1) * page_size
    # 查询指定数量的记录
    data = collection.find().skip(skip).limit(page_size)
    return data

# 所有表
@app.get("/")
async def index():
    tables=get_all_table_names()
    links = "\n".join([f"<a href='/tables/{table}'>{table}</a>" for table in tables])
    html_content= f"点击表名  即可查看里面的数据:\n  {links}   "
    html_content=html_content.replace('\n','<br>')
    return Response(content=html_content, media_type="text/html")

# 中转路由 把选择的表数据交付给视图进行渲染
@app.get("/tables/{table_name}")
async def table_data(table_name: str, page_num: int = 1, page_size: int = 10):
    data = get_page_data(table_name, page_num, page_size)
    # 渲染列表页
    html_content = list_page(data, page_num, page_size)
    return {"data": data}


# 列表页
app.include_router(list_router)

# 详情页
app.include_router(detail_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)