



import pandas as pd

import gradio as gr


# 盛满屏幕控制
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
"""
# 高亮背景色
def highlight(s:pd.DataFrame):

    success_css = 'background-color: green;'
    error_css = 'background-color: red;'
    pending_css = 'background-color: gray;'
    delay_css = 'background-color: '';'

    def apply_css(val):
        # 字符串类型
        if pd.api.types.is_string_dtype(val):
            return pending_css
        # bool False
        elif val == False:
            return error_css
        # bool True
        elif val == True:
            return success_css
        else:
        # 默认没有背景色
            return delay_css
    new_s=s.applymap(apply_css,)
    return new_s



from fastapi import APIRouter

router = APIRouter()


@router.get("/list_items")
async def list_items(data):
    df = pd.DataFrame(data)
    styler=df.style.apply(highlight, axis=None)
    with gr.Blocks(title='列表页',css=css) as demo:
        df1=gr.Dataframe(value=styler)
    return demo


