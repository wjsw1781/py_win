

import gradio as gr

from fastapi import APIRouter

router = APIRouter()



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


@router.get("/detail_item")
def detail_page(item):
    with gr.Blocks(title='监控爬虫进程以及进度',css=css,js='./click.js') as demo:

        with gr.Row(elem_id='global_switch' ,elem_classes='control_ele_area'):
            with gr.Column(elem_classes='control_ele_area'):
                # 一些全局开关  是否开启鼠标xy绘制线条  是否屏蔽所有事件
                gr.Checkbox(label='是否开启鼠标xy绘制线条',value=False,elem_id='is_draw_line')

            with gr.Column():
                gr.Checkbox(label='初步判定不可用:***',value=False,)

            with gr.Column():
                gr.Checkbox(label='来自up主:****',value=False,)

            with gr.Column():
                gr.Checkbox(label='视频长度:****',value=False,)

            with gr.Column():
                gr.Checkbox(label='投稿时间:****',value=False,)


        with gr.Row():
            with gr.Column(elem_classes='control_ele_area'):

                canbe_use_btn=gr.Radio(['不可用','可用'], label="视频是否可用")
                
                gr.Radio(["获取左上", "获取右下","停止尺寸标注"], label="视频尺寸", elem_id='video_size')

                gr.Radio(['开始水印标注','停止水印标注'], label="水印标注",elem_id='is_draw_shuiyin_area')

                with gr.Row(elem_id=''):
                    start_btn=gr.Button(value='前置片段删除',elem_id='start_btn')
                    end_btn=gr.Button(value='后置片段删除',elem_id='end_btn')

                submit=gr.Button(value='提交')


            with gr.Column(scale=2):
                gr.HTML(f'<iframe src={h5_url} style="width: 1000px; height: 1000px;"></iframe>')

            with gr.Column() as res:
                with gr.Row(elem_id=''):
                    canbe_use_res=gr.Text(placeholder='视频是否可用',show_label=False)

                with gr.Row(elem_id='video_size_res'):
                    left_bottom_res=gr.Text(placeholder='获取左上结果',show_label=False)
                    right_bottom_res=gr.Text(placeholder='获取右下结果',show_label=False)

                with gr.Row(elem_id='is_draw_shuiyin_area_res'):
                    warter_res=gr.Text(placeholder='获取水印下边距结果',show_label=False)
                
                with gr.Row(elem_id=''):
                    delet_pre=gr.Text(placeholder='前置片段删除至',show_label=False)
                    delet_end=gr.Text(placeholder='后置片段删除至',show_label=False)


                with gr.Row(elem_id=''):
                    submit_is_ok=gr.Text(placeholder='服务器判定提交参数是否合法',show_label=False)


        with gr.Row():
            with gr.Column(scale=2):
                slider=gr.Slider(label='进度条', minimum=0, maximum=length_seconds, step=1, value=0)

        with gr.Row():
            gr.Image(label='处理前视频截图',)
            gr.Image(label='处理前视频截图',)
            gr.Image(label='处理前视频截图',)
            gr.Image(label='处理前视频截图',)

        with gr.Row():
            gr.Image(label='处理后视频截图',)
            gr.Image(label='处理后视频截图',)
            gr.Image(label='处理后视频截图',)
            gr.Image(label='处理后视频截图',)

        canbe_uplaod_radio=gr.Radio(['不可以投稿','投稿'], label="是否可以投稿_后续可以添加投稿后抖音反响组件 粉丝增长情况组件 等")

        # 一些ui 函数 双向绑定  此时已经打通了前后端不用接住js那么复杂的运行时修改和获取值了
        start_btn.click(lambda x:seconds_to_time(x),inputs=slider,outputs=delet_pre)
        end_btn.click(lambda x:seconds_to_time(x),inputs=slider,outputs=delet_end)
        canbe_use_btn.change(lambda x:x,inputs=canbe_use_btn,outputs=canbe_use_res)

        def get_compents_values(left_bottom_res,right_bottom_res,warter_res,canbe_use_res,delet_pre,delet_end):
            res={
                "canbe_use_res":canbe_use_res,
                "left_bottom_res":left_bottom_res,
                "right_bottom_res":right_bottom_res,
                "warter_res":warter_res,
                "delet_pre":delet_pre,
                "delet_end":delet_end
            }
            if left_bottom_res=='':
                return "不合法 你是不是忘记复制了?"

            # 更新到mongo中

            return "可以的 后台马上剪辑 裁剪  抽帧!!!!!  太吊了"
        
        submit.click(get_compents_values,inputs=[left_bottom_res,right_bottom_res,warter_res,canbe_use_res,delet_pre,delet_end],outputs=submit_is_ok)

        def upload_ok(canbe_uplaod_radio):
            # 更新mongo中
            print("🚀 ~ canbe_uplaod_radio:  更新mongo中", canbe_uplaod_radio)

            pass

        canbe_uplaod_radio.change(upload_ok,inputs=canbe_uplaod_radio,outputs=None)
    return demo
        













