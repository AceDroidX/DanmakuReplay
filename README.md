# DanmakuReplay

使用方法：  
1. 将config.example.json重命名为config.json并修改里面的设置
2. 新建cookie.txt并填入您在B站的cookie信息（具体方法请自行搜索）
3. 安装依赖并运行
```
pip install -r requirements.txt
python main.py
```

参数解释：  
+ danmu_file_name：弹幕文件名，文件的数据结构参考danmu_file.example.json
+ danmu_start_time：开始发送的弹幕时间戳(单位毫秒)，对应弹幕文件里的time值
+ danmu_color：弹幕颜色，16777215为白色，65532为活动中的青色
+ danmu_interval：发弹幕的最小CD，在CD时间内的弹幕将被跳过
+ roomid：直播间房间号