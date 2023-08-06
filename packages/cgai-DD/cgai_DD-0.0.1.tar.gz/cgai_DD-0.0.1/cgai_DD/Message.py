# -*- coding:utf-8 -*-
import requests
import json


def sendMessage(webhook,text):
    """
    发送文本信息
    :param webhook: 钉钉机器人的webhook
    :param text: 发生的内容信息
    :return:
    """

    HEADERS = {
    "Content-Type": "application/json ;charset=utf-8 "
    }

    String_textMsg = {"msgtype": "text","text": {"content":text}}
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(webhook, data=String_textMsg, headers=HEADERS)
    return res.text
