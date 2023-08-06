#-*- coding:utf-8 -*-
"""
发送链接
"""
import json
import requests

def sendLink(webhook,messageUrl,title,text,picUrl=''):
    """
        发送网络链接
    :param webhook: 钉钉机器人的webhook
    :param messageUrl: 网络链接
    :param title: 标题
    :param text: 发生的内容信息
    :param picUrl: 显示图片链接
    :return:
    """

    HEADERS = {
    "Content-Type": "application/json ;charset=utf-8 "
    }

    String_textMsg = {"msgtype": "link",
                      "link": {
                          "title": title,
                          "text": text,
                          "picUrl":picUrl,
                          "messageUrl":messageUrl
                      },
                      "text": {"content":text}}
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(webhook, data=String_textMsg, headers=HEADERS)
    return res.text
