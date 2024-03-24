# -*- coding: utf-8 -*-
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
from utils.utils import *
# 准备一个b站视频

table_name='da_xing_jilupian'
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')
db = client.zhiqiang_hot
table=db[table_name]
video=table.find_one()
aid=video['aid']
bvid=video['bvid']
length=video['length']   #01:22
title=video['title']   #01:22

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
# 换算成秒 方便后面逻辑使用
length_seconds=time_to_seconds(length)  #01:22



# 生成一个html5播放链接
h5_url=preview_h5_video_url(aid=aid,bvid=bvid)

# pip install gradio -i https://pypi.tuna.tsinghua.edu.cn/simple 
css = """
.gradio-container-4-22-0{
    height: 100%;
    width:100%;
    max-width: 100%;
    min-width: 100%;

}
.container {
    height: 100%;
    width:100%;
    max-width: 100%;
    min-width: 100%;
}

#global_switch{
    z-index: 1000;
}
.control_ele_area{
    z-index: 1000;

}
"""


# 准备一个gradio画面
import gradio as gr

with gr.Blocks(title='监控爬虫进程以及进度',css=css,js='./click.js') as demo:
    # 一些全局开关  是否开启鼠标xy绘制线条  是否屏蔽所有事件
    with gr.Row(elem_id='global_switch'):
        gr.Checkbox(label='是否开启鼠标xy绘制线条',value=False,elem_id='is_draw_line')
    # 
    with gr.Row():
        with gr.Column(elem_classes='control_ele_area'):
            gr.Radio(["获取上边距", "获取下边距", "获取左边距", "获取右边距",'获取完成'], label="视频尺寸", elem_id='video_size')

            gr.Radio(['开启水印标注','关闭水印标注'], label="水印标注",elem_id='is_draw_shuiyin_area')


        with gr.Column(scale=2):
            gr.HTML(f'<iframe src={h5_url} style="width: 1000px; height: 1000px;"></iframe>')

        with gr.Column():
            with gr.Row(elem_id='video_size_res'):
                gr.Text(placeholder='获取上边距结果',show_label=False)
                gr.Text(placeholder='获取下边距结果',show_label=False)
                gr.Text(placeholder='获取左边距结果',show_label=False)
                gr.Text(placeholder='获取右边距结果',show_label=False)
                gr.Text(placeholder='获取完成结果',show_label=False)

            with gr.Row(elem_id='is_draw_shuiyin_area_res'):
                gr.Text(placeholder='获取水印下边距结果',show_label=False)
                gr.Text(placeholder='是否已完成水印的工作',show_label=False)




    with gr.Row():
        with gr.Column():
            gr.Text(label='进度条相关')

        with gr.Column(scale=2):
            gr.Slider(label='进度条', minimum=0, maximum=length_seconds, step=1, value=0)

        with gr.Column():
            gr.Text(label='进度条最终结果')



demo.launch(server_port=5200,server_name="127.0.0.1",)
    













