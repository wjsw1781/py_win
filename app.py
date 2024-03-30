import pandas as pd
import streamlit as st
from pages import  detail_page,list_page


from pymongo import MongoClient

table_name='da_xing_jilupian'
client = MongoClient(host='139.196.158.152', port=27017, username='root', password='1213wzwz', authSource='admin')

db = client.zhiqiang_hot
tables = db.list_collection_names()
page_size=10

st.set_page_config(layout="wide")
st.title("增删改查mongo数据库  + 特定组件组合")


"""
几个状态变量
choose_table
page_number
page_size
data

"""
st.session_state['choose_table']=None
st.session_state['page_number']=None
st.session_state['page_size']=30
st.session_state['data']={}


@st.cache_data
def get_data_from_mongodb_by_page(table_name,page_number, page_size=page_size):
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
    with st.sidebar:
        selected_table = st.radio(label='选择表', options=tables)

        if selected_table != st.session_state.get('choose_table'):
            st.session_state['choose_table'] = selected_table



# 组件列表
def components():

    pass

# 列表页
def list_part():


    choose_table=st.session_state['choose_table']
    page_size = st.number_input(label='每页显示数量', min_value=1, step=1, value=st.session_state['page_size'])
    total_pages= db[choose_table].count_documents({})//page_size+1
    page_number = st.slider(label='页码', min_value=1, max_value=total_pages, value=1, step=1)
    
    # 如果页码发生变化，更新数据
    if page_number != st.session_state.get('page_number') or page_size != st.session_state.get('page_size'):
        st.session_state['page_number'] = page_number
        st.session_state['page_size'] = page_size
    
    st.session_state['data'] = get_data_from_mongodb_by_page(choose_table, page_number, page_size)
    editable_df:pd.DataFrame=st.data_editor(st.session_state['data'] )

    if not(editable_df.equals(st.session_state['data'])) :
        diff_rows = editable_df.compare(st.session_state['data'])
        table=db[choose_table]
        # 更新数据库
        for index, row in diff_rows.iterrows():
            obj=row.to_dict()
            keys=list(obj.keys())
            col_name=keys[0][0]
            new_value=obj[keys[0]]
            old_value=obj[keys[1]]
            _id=editable_df.loc[index]['_id']
            print( f'{_id}    {col_name}  {old_value}---->{new_value}', )
            table.update_one({'_id': _id}, {'$set': {col_name: new_value}})
        

        # 保持最新状态
        st.session_state['data']=editable_df


# 详情页
def detail_part():
    
    pass


def main():
    # 侧边栏
    db_tables()
   
    # 组件列表
    components()



    # 主体内容
    list, detail = st.columns(2,gap='small')
    with list:
        list_part()


    with detail:
        detail_part()



    pass


if __name__ == "__main__":
    main()