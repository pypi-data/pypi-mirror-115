#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re

from aumtest.common import Var
from aumtest.drivers.driver_base_app import DriverBaseApp
from aumtest.utils.opcv_utils import OpencvUtils
from aumtest.runner.action_executor_base import ActionExecutorBase


class ActionExecutorMinium(ActionExecutorBase):

    def _miniumClick(self,action):
        # 点击指定组件
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.get_current_page().get_element(" + action.step[12:len(action.step) - 1] + ").click()"
            exec(execStr)
        except:
            raise TypeError("元素没找到:"+execStr)

    def _miniumNavigateTo(self, action):
        #以导航的方式跳转到指定页面(不能跳到 tabbar 页面。支持相对路径和绝对路径, 小程序中页面栈最多十层)
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.navigate_to(" + action.step[17:len(action.step) - 1] + ")"
            exec(execStr)
        except:
            raise TypeError("导航到指定页面出错:",execStr)

    def _miniumInput(self, action):
        # input & textarea 组件输入文字
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.get_current_page().get_element(\""+self._getParms(action,0)+"\").input(\"" + self._getParms(action, 1 ) + "\")"
            exec(execStr)
        except:
            raise TypeError("组件输入文字出错:",execStr)

    def _miniumScrollTo(self, action):
        #  滚动到指定高度
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.get_current_page().scroll_to("+action.step[15:len(action.step) - 1]+")"
            exec(execStr)
        except:
            raise TypeError("组件输入文字出错:", execStr)

    def _miniumGetElement(self, action):
        # 在当前控件内查询控件, 如果匹配到多个结果, 则返回第一个匹配到的结果
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.get_current_page().get_element(" + action.step[17:len(action.step) - 1] + ")"
            element = eval(execStr)
            if element:
                return element
            else:
                return False
        except:
            raise TypeError("元素没找到:" + execStr)

    def _miniumGetElements(self, action):
        # 在当前控件内查询控件, 并返回一个或者多个结果
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.get_current_page().get_elements(" + action.step[18:len(action.step) - 1] + ")"
            elements = eval(execStr)
            if elements:
                return elements
            else:
                return False
        except:
            raise TypeError("元素没找到:" + execStr)

    def _miniumWaitFor(self, action):
        #   等待直到指定的条件成立
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.get_current_page().wait_for(" + action.step[14:len(action.step) - 1] + ")"
            eval(execStr)
        except:
            raise TypeError("wait_for出错了:" + execStr)

    def _miniumElementIsExists(self, action):
        #   在当前页面查询控件是否存在
        execStr = ''
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.get_current_page().element_is_exists(" + action.step[22:len(action.step) - 1] + ")"
            result = eval(execStr)
            return result
        except:
            raise TypeError("wait_for出错了:", execStr)

    def _miniumGoHome(self, action):
        #   跳转到小程序首页
        execStr = ''
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.app.go_home()"
            result = eval(execStr)
        except:
            raise TypeError("go_home出错了:", execStr)

    def _miniumTrigger(self, action):
        # 触发元素事件
        execStr = ''
        try:
            action.step = action.step.strip()
            action.step = action.step[14:len(action.step)-1]
            selector = action.step[0:action.step.index(',')]
            triggerParam = action.step[action.step.index(',')+1:len(action.step)]
            element = Var.instance.app.get_current_page().get_element(selector)
            if not element:
                raise Exception("沒有找到元素:", execStr)
            element.trigger(triggerParam[0:triggerParam.index(',')], triggerParam[triggerParam.index(',')+1:])
        except:
            raise TypeError("miniumTrigger:" ,execStr)

    def _miniumActionSheet(self,action):
        #   处理上拉菜单
        execStr = ''
        try:
            action.step = action.step.strip()
            execStr = "Var.instance.native.handle_action_sheet(" + action.step[18:len(action.step) - 1] + ")"
            eval(execStr)
        except:
            raise TypeError("miniumActionSheet:", execStr)

    def _miniumAllowGetLocation(self, action):
        # 处理获取位置信息确认弹框
        execStr = ''
        try:
            action.step = action.step.strip()
            Var.instance.native.allow_get_location()
        except:
            raise TypeError("miniumAllowGetLocation:", execStr)

    def _miniumMapSelectLocation(self, action):
        #原生地图组件选择位置
        execStr = ''
        try:
            action.step = action.step.strip()
            Var.instance.native.map_select_location(self._getParms(action,0))
        except:
            raise TypeError("miniumMapSelectLocation:", execStr)

    def _input(self, action):
        '''
        :param action:
        :return:
        '''
        text = self._getParms(action, 1)
        element = self._getElement(action)
        DriverBaseApp.input(element, text)

    def _click(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                x = img_info['x']
                y = img_info['y']
                DriverBaseApp.tap(x, y)
            else:
                raise Exception("Can't find element {}".format(parms))
        else:
            element = self._getElement(action)
            element.click()

    def _check(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
            else:
                raise Exception("Can't find element {}".format(parms))
        else:
            self._getElement(action)

    def _ifiOS(self, action):
        '''
        :param action:
        :return:
        '''
        if Var.desired_caps.platformName.lower() == 'ios':
            return True
        return False

    def _ifAndroid(self, action):
        '''
        :param action:
        :return:
        '''
        if Var.desired_caps.platformName.lower() == 'android':
            return True
        return False

    def _getText(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        text = DriverBaseApp.get_text(element)
        return text

    def _getElement(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        # if Var.driver == 'appium':
        #     from appium.webdriver import WebElement
        # if Var.driver == 'macaca':
        #     from macaca.webdriver import WebElement

        # if isinstance(parms, WebElement):
        #     element = parms
        # else:
        #     element = DriverBaseApp.find_elements_by_key(key=parms, timeout=Var.time_out, interval=Var.interval)
        element = Var.instance.app.get_current_page().get_element(''.join(action.parms))
        if not element:
            raise Exception("Can't find element {}".format(parms))
        return element

    def _getElements(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=Var.time_out, interval=Var.interval,
                                                      not_processing=True)
        if not elements:
            raise Exception("Can't find element {}".format(parms))
        return elements

    def _isExist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        result = True
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
            else:
                result = False
        else:
            elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=Var.time_out, interval=Var.interval, not_processing=True)
            result = bool(elements)
        return result

    def _isNotExist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        result = False
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                result = True
        else:
            elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=0, interval=Var.interval, not_processing=True)
            result = bool(elements)
        return not result

    def _ocrAnalysis(self,image_name, match_image):
        '''
        :param image_name:
        :param match_image:
        :return:
        '''
        try:
            if not isinstance(match_image, str):
                return False
            if not os.path.isfile(match_image):
                return False

            image_dir = os.path.join(Var.snapshot_dir, 'screenshot')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            base_image = os.path.join(image_dir, '{}'.format(image_name))
            Var.instance.save_screenshot(base_image)
            height = Var.instance.get_window_size()['height']

            orcimg = OpencvUtils(base_image, match_image, height)
            img_info = orcimg.extract_minutiae()
            if img_info:
                return img_info
            else:
                return None
        except:
            return False