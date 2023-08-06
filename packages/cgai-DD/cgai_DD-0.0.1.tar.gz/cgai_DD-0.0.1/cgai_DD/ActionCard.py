# -*- coding:utf-8 -*-
import requests
import json


def sendActionCard(webhook,markdown:str,showTitle,singleTitle,singleURL='',btnOrientation:int=0):
    """
    发送文本信息
    :param webhook: 钉钉机器人的webhook
    :param markdown: 发送的markdown格式
    :param showTitle: 手机屏幕弹出信息显示标题
    :param singleTitle: 子标题
    :param singleURL: 链接

    :param btnOrientation: 0按钮竖直排列，1横向排列
    :return:
    """

    HEADERS = {
    "Content-Type": "application/json ;charset=utf-8 "
    }

    String_textMsg = {"msgtype": "actionCard",
                      "actionCard": {"title":showTitle,
                                     "text":markdown,
                                     "btnOrientation":str(btnOrientation),
                                     "singleTitle":singleTitle,
                                     "singleURL":singleURL}
                      }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(webhook, data=String_textMsg, headers=HEADERS)
    return res.text



def sendActionsCard(webhook,markdown:str,showTitle,singleTitle,singleURL='',btns:list=[],btnOrientation:int=0):
    """
    发送文本信息
    :param webhook: 钉钉机器人的webhook
    :param markdown: 发送的markdown格式
    :param showTitle: 手机屏幕弹出信息显示标题
    :param btns: [data,data,...]
                data格式为:{"title":xxxx,"actionURL":url}
    :param btnOrientation: 0按钮竖直排列，1横向排列
    :return:
    """

    HEADERS = {
    "Content-Type": "application/json ;charset=utf-8 "
    }

    String_textMsg = {"msgtype": "actionCard",
                      "actionCard": {"title":showTitle,
                                     "text":markdown,
                                     "btnOrientation":str(btnOrientation),
                                     "btns":btns}
                      }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(webhook, data=String_textMsg, headers=HEADERS)
    return res.text



def sendFreeCard(webhook,links:list):
    """
    发送文本信息
    :param webhook: 钉钉机器人的webhook
    :param links: 链接信息[data,data,...]
                        data格式为: {"title":xxx,"messageURL":"http://xxx","picURL":"http://xxx"}
                            title:标题
                            messageURL:链接
                            picURL:图片链接
    :return:
    """

    HEADERS = {
    "Content-Type": "application/json ;charset=utf-8 "
    }

    String_textMsg = {"msgtype": "feedCard",
                      "feedCard": {
                          "links": links
                      }
                      }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(webhook, data=String_textMsg, headers=HEADERS)
    return res.text
















