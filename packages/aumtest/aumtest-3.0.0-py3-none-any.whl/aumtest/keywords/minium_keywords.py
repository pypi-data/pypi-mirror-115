#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def return_keywords(driver):
    keywords_minium= [
        "miniumClick",  # 点击元素
        "miniumNavigateTo",  # 以导航的方式跳转到指定页面(不能跳到 tabbar 页面。支持相对路径和绝对路径, 小程序中页面栈最多十层)
        "miniumInput",  # input & textarea 组件输入文字
        "miniumWaitFor",    # 等待直到指定的条件成立
        "miniumElementIsExists",     # 在当前页面查询控件是否存在
        "miniumGoHome",  # 跳转到小程序首页
        "miniumScrollTo",   # TODO:滚动到指定高度 (第一个参数:滚动到页面高度位置,第二个参数:滚动时间(ms))
        "miniumGetElement", # TODO:在当前控件内查询控件, 如果匹配到多个结果, 则返回第一个匹配到的结果
        "miniumGetElements",  # TODO:在当前控件内查询控件, 并返回一个或者多个结果
        "miniumTrigger",  # TODO:触发元素事件
        "miniumActionSheet",  # TODO:处理上拉菜单
        "miniumAllowGetLocation",  # TODO:处理获取位置信息确认弹框
        "miniumMapSelectLocation", # TODO:原生地图组件选择位置
    ]
    keywords = list(set(keywords_minium))
    return keywords
