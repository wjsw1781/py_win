window.onload = () => {
    // 填写视频尺寸功能
    function fill_video_size(x, y) {
        let all_top_butoome_left_right = Array.from(document.querySelector('#video_size').querySelectorAll('input'))
        let now_ele = all_top_butoome_left_right.filter((item, index) => item.checked == true)
        let now_index = all_top_butoome_left_right.indexOf(now_ele)

        let all_top_butoome_top_bottom_res = Array.from(document.querySelector('#video_size_res').querySelectorAll('input'))
        all_top_butoome_top_bottom_res[now_index].value = x + 'x' + y

    }





    // 全局开关显示鼠标
    window.is_draw_line = document.querySelector("#is_draw_line").querySelector('input')


    // 移动鼠标显示
    window.xy_mousemove = document.createElement('div');
    xy_mousemove.style.position = 'absolute';
    xy_mousemove.style.top = '0';
    xy_mousemove.style.left = '0';
    xy_mousemove.style.width = '100%';
    xy_mousemove.style.height = '100%';
    document.body.appendChild(xy_mousemove);
    document.addEventListener('mousemove', function (event) {

        var x = event.clientX;
        var y = event.clientY;

        if (!is_draw_line.checked) {
            // 表明这里要开始标注了 页面上的所有不能被点击  
            xy_mousemove.style.zIndex = '-1';

        }

        var verticalLine = document.createElement('div');
        verticalLine.style.position = 'absolute';
        verticalLine.style.left = x + 'px';
        verticalLine.style.width = '1px';
        verticalLine.style.height = '100%';
        verticalLine.style.backgroundColor = 'red';

        // 创建水平线条
        var horizontalLine = document.createElement('div');
        horizontalLine.style.position = 'absolute';
        horizontalLine.style.top = y + 'px';
        horizontalLine.style.width = '100%';
        horizontalLine.style.height = '1px';
        horizontalLine.style.backgroundColor = 'blue';

        // 清楚 container 中所有
        while (xy_mousemove.firstChild) {
            xy_mousemove.removeChild(xy_mousemove.firstChild);
        }
        xy_mousemove.appendChild(verticalLine);
        xy_mousemove.appendChild(horizontalLine);



    });

    // 点击鼠标时
    document.addEventListener('click', function (event) {
        var x = event.clientX;
        var y = event.clientY;
        console.log(x, y)
    })




}