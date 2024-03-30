import functools
import pandas as pd
import streamlit as st
from pages import  detail_page,list_page


from pymongo import MongoClient


st.set_page_config(layout="wide")
st.title("增删改查mongo数据库  + 特定组件组合")


"""
几个状态变量
choose_table
page_number
page_size
data_df
selected_rows

"""
st.session_state['choose_table']=None
st.session_state['page_number']=1
st.session_state['page_size']=30
st.session_state['data_df']=pd.DataFrame({})
st.session_state['selected_rows']=pd.DataFrame({})



@st.cache_resource
def get_db():
    client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

    db = client.zhiqiang_hot
    return db

@st.cache_data
def get_data_from_mongodb_by_page(table_name,page_number, page_size=5):
    db = get_db()
    table = db[table_name]
    skip_count = (page_number - 1) * page_size
    
    # 查询数据并应用分页逻辑
    cursor = table.find().skip(skip_count).limit(page_size)
    page_data=list(cursor)
    print(len(page_data))
    
    return pd.DataFrame(page_data)

# 数据列表
def db_tables():
    # 获取数据库中所有表名
    tables=get_db().list_collection_names()
    with st.sidebar:
        selected_table = st.radio(label='选择表', options=tables)
        if selected_table != st.session_state.get('choose_table'):
            st.session_state['choose_table'] = selected_table



# 列表页
def list_part():

    db=get_db()
    choose_table=st.session_state['choose_table']
    total_pages= db[choose_table].count_documents({})//st.session_state['page_size']+1

    col1,col2=st.columns(2)
    with col1:
        page_number=st.slider('页码', min_value=1, max_value=total_pages, step=1, value=st.session_state.get('page_number') )
    with col2:  
        page_size = st.number_input(label='每页显示数量', min_value=1, step=1, value=st.session_state['page_size'])
        
    
    # 如果页码发生变化，更新数据
    if page_number != st.session_state.get('page_number') or page_size != st.session_state.get('page_size'):
        st.session_state['page_number'] = page_number
        st.session_state['page_size'] = page_size
    
    # 上面的变动引起重新渲染 导致这里发生了不一致
    data_df = get_data_from_mongodb_by_page(choose_table, page_number, page_size)
    if data_df.values!=st.session_state.get('data_df').values:
        st.session_state['data_df'] = data_df


    df_with_selections = data_df.copy()
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(df_with_selections,hide_index=True,
                               column_config={"Select": st.column_config.CheckboxColumn(required=True),
                               },
                               num_rows="Dynamic",
                               height=800)

    selected_rows = edited_df[edited_df.Select]
    if selected_rows.values!=st.session_state.get('selected_rows').values:
        st.session_state['selected_rows'] = selected_rows

# 详情页
def detail_part():
    # 针对b站的水印进行标注的详情页
    selected_rows:pd.DataFrame=st.session_state['selected_rows']
    selected_rows_obj=selected_rows.values.tolist()
    filed_name=selected_rows.columns.to_list()
    if len(selected_rows_obj)==0:
        return
    if 'bvid' not in filed_name:
        return
    
    
    bvid_indexof=filed_name.index('bvid')
    bvid=selected_rows_obj[0][bvid_indexof]
    videod_url=f'http://player.bilibili.com/player.html?bvid={bvid}'
    iframe_table=f"""<iframe id="my-iframe" src="{videod_url}" width="100%" height="800px" frameborder="0"></iframe>"""

    st.markdown(iframe_table,unsafe_allow_html=True)

    # 图片显示

    pass


def main():
    # 侧边栏
    db_tables()
   
  

    # 主体内容
    list, detail = st.columns(2,gap='small')
    with list:
        list_part()


    with detail:
        detail_part()



    pass


if __name__ == "__main__":
    main()
