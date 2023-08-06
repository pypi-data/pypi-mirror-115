# -*- coding:utf-8 -*-
import requests
import json


def sendMarkdown(webhook,markdown:str,showTitle,atMobiles=[],atUserIds=[],isAtAll=False):
    """
    发送文本信息
    :param webhook: 钉钉机器人的webhook
    :param markdown: 发送的markdown格式
    :param showTitle: 手机屏幕弹出信息显示标题
    :param atMobiles: 要@人员的手机号
    :param atUserIds: 要@人员的user id
    :param isAtAll: 是否@所有人
    :return:
    """

    HEADERS = {
    "Content-Type": "application/json ;charset=utf-8 "
    }

    String_textMsg = {"msgtype": "markdown",
                      "markdown": {"title":showTitle,
                                   "text":markdown},
                      "at":{"atMobiles":[],
                            "atUserIds":[],
                            "isAtAll":isAtAll}}
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(webhook, data=String_textMsg, headers=HEADERS)
    return res.text
