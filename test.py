import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd




# 创建一个Dash应用实例
app = dash.Dash(__name__)

# 第一个UI对应的布局和路由函数
def layout1():
    # 生成一些示例数据
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [10, 20, 30, 40, 50],
        "category": ["A", "B", "A", "B", "A"]
    })
    # 定义布局
    layout = html.Div([
        html.H1("UI 1 示例"),
        dcc.Graph(
            id='example-graph-1',
            figure=px.scatter(df, x='x', y='y', color='category', title='Scatter Plot 1')
        ),
        html.Div("这是UI 1 的一个简单示例，展示了一个交互式散点图。")
    ])
    return layout

# 第二个UI对应的布局和路由函数
def layout2():
    # 生成一些示例数据
    df = pd.DataFrame({
        "x": [5, 4, 3, 2, 1],
        "y": [50, 40, 30, 20, 10],
        "category": ["A", "B", "A", "B", "A"]
    })
    # 定义布局
    layout = html.Div([
        html.H1("UI 2 示例"),
        dcc.Graph(
            id='example-graph-2',
            figure=px.scatter(df, x='x', y='y', color='category', title='Scatter Plot 2')
        ),
        html.Div("这是UI 2 的一个简单示例，展示了一个交互式散点图。")
    ])
    return layout

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-2':
        return layout2()
    else:
        return html.Div("404 - 页面未找到")

# 设置整体布局
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)
