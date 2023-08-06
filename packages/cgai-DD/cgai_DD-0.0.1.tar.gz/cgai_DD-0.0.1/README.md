# cgai-DD

#### 介绍
钉钉群机器人的python API接口



#### 安装教程

```python
pip install cgai-DD
```

#### 注意  

1.仅支持python3  
2.发送的图片路径必须是网络路径  
3.发送的图片格式图必须是jpg格式

#### 使用案例

```python
import cgai_DD as dd
```

```python
WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxx'
```

###### 发送文本信息
```python
dd.sendMessage(WEBHOOK,'发送的内容')
```


###### 发送连接
```python
message_url = r'https://zhuanlan.zhihu.com/p/391348944'
title = 'CGAI-time'
text = 'cgai-time一个简单又实用的时间日期处理python库'
pic_url = 'https://obohe.com/i/2021/08/06/ikclyn.jpg'

dd.sendLink(WEBHOOK,message_url,title,text,pic_url)
```


###### 发送markdown
```python
pic_url = 'https://obohe.com/i/2021/08/06/e1qrsr.png'
markdown = """
## cgai-time一个简单又实用的时间日期处理python库
体育老师再也不用担心我算不出时间了
![img](https://obohe.com/i/2021/08/06/ikclyn.jpg)
###### 帮助说明 [链接](https://zhuanlan.zhihu.com/p/391348944)
"""
title = 'cgai-time分享'

dd.sendMarkdown(WEBHOOK,markdown,title)
```


###### 发送ActionCard
```python
markdown = """
![img](https://obohe.com/i/2021/08/06/ikclyn.jpg)
### cgai-time
"""
showTitle = 'cgai-time'
singleTitle = '阅读文章'
url = 'https://zhuanlan.zhihu.com/p/391348944'
dd.sendActionCard(WEBHOOK,markdown,showTitle,singleTitle,url,btnOrientation=1)


btns = [{"title":'链接1',"actionURL":url},{"title":'链接2',"actionURL":url}]
dd.sendActionsCard(WEBHOOK,markdown,showTitle,singleTitle,url,btns,btnOrientation=0)

```

###### 发送Freecard
```python
url = 'https://zhuanlan.zhihu.com/p/391348944'
pic_url = 'https://obohe.com/i/2021/08/06/ikclyn.jpg'

links = [{"title":"标题1","messageURL":url,"picURL":pic_url},
         {"title":"标题2","messageURL":url,"picURL":pic_url}]

dd.sendFreeCard(WEBHOOK,links)
```



