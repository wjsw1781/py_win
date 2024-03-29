pyhton3.8
pip install loguru requests pywebio DrissionPage bilibili-api-python httpx moviepy==1.0.3 numpy==1.21.5 opencv_python==4.5.5.62   -i https://pypi.tuna.tsinghua.edu.cn/simple  


使用一个工具似乎更容易控制浏览器  当然js的能力也要建设起来!!!!
但是它太好用了 cdp似乎做的事情更牛逼 更确定!!!



爬取
筛选
人工标记审核平台
剪辑
上传


<!-- 关于可视化审核平台的初步设想 -->
未来肯定会有很多表作为业务线出现 本质上都是对状态的查看  以及修改 
但是不同的表需要的查看和修改逻辑并不一样  但本质上都是以字段为单位进行修改
所以可以抽离出三个实体

原始表格以及字段内容
展示表格和字段的组件
最终detail页结果

数据+组件=detail页

未来只是新增组件和数据源   即可

比如业务
        显示s3上的图片并进行逐个审核
        显示资产详情
        标注视频尺寸 水印
本质上都是对状态的查看  以及修改




