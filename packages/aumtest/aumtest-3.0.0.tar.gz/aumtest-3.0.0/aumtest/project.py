# coding:utf-8
'''
@File    : project.py
@Author  : TM_QA
'''

import os
import sys
import time
import math
import unittest
import threading
import requests
from aumtest.common import *
from aumtest.utils import *
from aumtest.keywords import keywords,minium_keywords
from aumtest.runner.run_case import RunCase
from aumtest.drivers.driver_base_app import DriverBaseApp
from aumtest.drivers.driver_base_web import DriverBaseWeb
from aumtest.result.test_runner import TestRunner



class Project(object):

    def __init__(self, index=0, workers=1, path='.'):

        self._index = index
        self._workers = workers
        self._root = path
        self._init_project()
        self._init_config()
        self._init_logging()
        self._analytical_testcase_file()
        self._analytical_common_file()
        self._init_data()
        self._init_testcase_suite()

    def _init_project(self):

        if not os.path.isdir(self._root):
            raise Exception('No such directory: {}'.format(self._root))
        if self._root == '.':
            self._root = os.getcwd()
        Var.root = self._root
        sys.path.append(Var.root)
        sys.path.append(os.path.join(Var.root, 'Scripts'))
        Var.global_var = Dict()
        Var.extensions_var = Dict()
        Var.common_var = Dict()
        Var.common_func = Dict()

    def _init_config(self):

        self._config = analytical_file(os.path.join(Var.root, 'config.yaml'))
        Var.driver = self._config.driver
        Var.re_start = self._config.reStart
        Var.save_screenshot = self._config.saveScreenshot
        Var.time_out = self._config.timeOut
        Var.test_case = self._config.testcase
        Var.desired_caps = Dict()
        for configK, configV in self._config.desiredCapabilities.items():
            Var.desired_caps[configK] = configV

        if not Var.driver or Var.driver.lower() not in ['appium', 'macaca', 'selenium','minium']:
            raise ValueError('Missing/incomplete configuration file: config.yaml, No driver type specified.')

        if not Var.time_out or not isinstance(Var.time_out, int):
            Var.time_out = 10
        if Var.driver == 'minium':
           if not Var.desired_caps.wxProjectPath or not Var.desired_caps.wxDevToolPath:
              raise ValueError('wxProjectPath or wxDevToolPath capability is expected')
        elif Var.driver != 'selenium':
            if not Var.desired_caps.platformName:
                raise ValueError('Missing/incomplete configuration file: config.yaml, No platformName type specified.')
            DriverBaseApp.init()
        else:
            if not Var.desired_caps.browser or Var.desired_caps.browser not in ['chrome', 'safari', 'firefox', 'ie', 'opera', 'phantomjs']:
                raise ValueError('browser parameter is illegal!')

    def _init_logging(self):
        if Var.driver == 'minium':
            info=""
        elif Var.driver != 'selenium':
            # 重置udid
            if self._workers > 1:
                if isinstance(Var.desired_caps.udid, list):
                    if not Var.desired_caps.udid:
                        raise Exception('Can‘t find device, udid("{}") is empty.'.format(Var.desired_caps.udid))
                    if self._index >= len(Var.desired_caps.udid):
                        raise Exception('the number of workers is larger than the list of udid.')
                    if not Var.desired_caps.udid[self._index]:
                        raise Exception('Can‘t find device, udid("{}") is empty.'.format(Var.desired_caps.udid[self._index]))
                    devices = DevicesUtils(Var.desired_caps.platformName, Var.desired_caps.udid[self._index])
                    Var.desired_caps['udid'], info = devices.device_info()
                else:
                    raise Exception('the udid list is not configured properly.')
            else:
                if isinstance(Var.desired_caps.udid, list):
                    if Var.desired_caps.udid:
                        devices = DevicesUtils(Var.desired_caps.platformName, Var.desired_caps.udid[0])
                    else:
                        devices = DevicesUtils(Var.desired_caps.platformName, None)
                else:
                    devices = DevicesUtils(Var.desired_caps.platformName, Var.desired_caps.udid)
                Var.desired_caps['udid'], info = devices.device_info()

        else:
            info = Var.desired_caps.browser

        thr_name = threading.currentThread().getName()
        report_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        report_child = "{}_{}_{}".format(info, report_time, thr_name)
        Var.report = os.path.join(Var.root, "Report", report_child)
        if not os.path.exists(Var.report):
            os.makedirs(Var.report)
            os.makedirs(os.path.join(Var.report, 'resource'))

    def _analytical_testcase_file(self):

        log_info('******************* analytical config *******************')
        for configK, configV in self._config.items():
            log_info(' {}: {}'.format(configK, configV))
        log_info('******************* analytical testcase *******************')
        testcase = TestCaseUtils()
        self._testcase = testcase.test_case_path(Var.root, Var.test_case)
        log_info(' case: {}'.format(len(self._testcase)))
        for case in self._testcase:
            log_info(' {}'.format(case))

    def _analytical_common_file(self):

        log_info('******************* analytical common *******************')
        common_dir = os.path.join(Var.root, "Common")
        for rt, dirs, files in os.walk(common_dir):
            if rt == common_dir:
                self._load_common_func(rt, files)
            elif Var.desired_caps.platformName and (rt.split(os.sep)[-1].lower() == Var.desired_caps.platformName.lower()):
                self._load_common_func(rt, files)
        for commonk, commonv in Var.common_func.items():
            log_info(' {}: {}'.format(commonk, commonv))

    def _load_common_func(self,rt ,files):

        for f in files:
            if not f.endswith('yaml'):
                continue
            for commonK, commonV in analytical_file(os.path.join(rt, f)).items():
                Var.common_func[commonK] = commonV

    def _init_data(self):

        data = analytical_file(os.path.join(Var.root, 'data.yaml'))
        dict = Dict(data)
        Var.extensions_var['variable'] = dict.variable
        Var.extensions_var['resource'] = dict.resource
        Var.extensions_var['keywords'] = dict.keywords
        if not Var.extensions_var.variable:
            Var.extensions_var['variable'] = Dict()
        if not Var.extensions_var.resource:
            Var.extensions_var['resource'] = Dict()
        if not Var.extensions_var.keywords:
            Var.extensions_var['keywords'] = Dict()
        # 注册全局变量
        log_info('******************* register variable *******************')
        for key, value in Var.extensions_var.variable.items():
            Var.extensions_var.variable[key] = value
            log_info(' {}: {}'.format(key, value))
        # 解析文件路径
        log_info('******************* register resource *******************')
        for resource, path in Var.extensions_var.resource.items():
            resource_file = os.path.join(Var.root, path)
            if not os.path.isfile(resource_file):
                log_error('No such file or directory: {}'.format(resource_file), False)
                continue
            Var.extensions_var.resource[resource] = resource_file
            log_info(' {}: {}'.format(resource, resource_file))
        # 注册关键字
        log_info('******************* register keywords *******************')
        Var.default_keywords_data = keywords.return_keywords(Var.driver)
        Var.new_keywords_data = Var.extensions_var.keywords
        Var.minium_keywords_data = minium_keywords.return_keywords(Var.driver)

        for key in Var.extensions_var.keywords:
            log_info(' {}'.format(key))

    def _init_testcase_suite(self):

        self._suite = []
        # 线程数大于用例数量时，取用例数
        if 1 < self._index > len(self._testcase):
            self._workers = len(self._testcase)
            if self._index == len(self._testcase):
                return
        if self._workers > 1:
            i = self._index
            n = self._workers
            l = len(self._testcase)
            self._testcase = self._testcase[math.floor(i / n * l):math.floor((i + 1) / n * l)]
        for case_path in self._testcase:
            test_case = analytical_file(case_path)
            test_case['test_case_path'] = case_path
            Var.case_info = test_case
            subsuite = unittest.TestLoader().loadTestsFromTestCase(RunCase)
            self._suite.append(subsuite)
            Var.case_info = None

    def start(self):

        if not self._suite:
            return None
        # 组装启动参数
        log_info('******************* analytical desired capabilities *******************')
        Var.desired_capabilities = Dict({
            'driver': Var.driver.lower(),
            'timeOut': Var.time_out,
            'desired': Var.desired_caps,
            'index': self._index,
            'root': self._root
        })
        # 启动服务
        if Var.driver == 'minium':
            import minium
            Var.instance = minium.Minium({
                "project_path": Var.desired_caps.wxProjectPath,  # 小程序项目目录地址
                "dev_tool_path": Var.desired_caps.wxDevToolPath  # 开发者工具cli地址，如果没有修改过默认安装路径可不填此项
            })
        elif Var.driver != 'selenium':
            server = ServerUtilsApp(Var.desired_capabilities)
            Var.instance = server.start_server()
        elif not Var.re_start:
            server = ServerUtilsWeb(Var.desired_capabilities)
            Var.instance = server.start_server()
            DriverBaseWeb.init()
        else:
            server = None
        # 用例运行
        suite = unittest.TestSuite(tuple(self._suite))
        runner = TestRunner()
        runner.run(suite)
        # 结束服务
        if Var.driver == 'minium':
            if Var.instance:
                ""
                # Var.instance.shutdown()
        elif Var.driver != 'selenium':
            server.stop_server()
        elif not Var.re_start:
            server.stop_server(Var.instance)

        # 打印失败结果
        if Var.all_result:
            if Var.all_result.errorsList:
                log_info(' Error case:')
            for error in Var.all_result.errorsList:
                log_error(error, False)

            if Var.all_result.failuresList:
                log_info(' Failed case:')
            for failure in Var.all_result.failuresList:
                log_error(failure, False)
        return Var.all_result

    # @staticmethod
    # def push_report():
    #     path = "./Report"
    #     # 获取路径下的所有文件
    #     dirs = os.listdir(path)
    #     dir_list = {}
    #     # 遍历所有文件
    #     for d in dirs:
    #         # 获取文件的创建时间
    #         ctime = os.path.getctime(os.path.join(path, d))
    #         dir_list[ctime] = d
    #     # 取最大的时间
    #     max_ctime = max(dir_list.keys())
    #     # 时间最新的文件名
    #     dir_name = dir_list[max_ctime]
    #     # remote_path 远程服务器地址
    #     remote_path = "/opt/aumtest/Report"
    #     # file_path 本地文件夹路径
    #     local_path = os.path.join(path, dir_name)
    #     # 上传文件至服务器
    #     a = f'sshpass -p test@Market scp -r {local_path} root@172.24.255.76:{remote_path}'
    #     os.popen(a)
    #     time.sleep(2)
    #     report_link = "http://172.24.255.76:7489/" + dir_name + "/report.html"
    #     robot_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cc414b17-4d5e-4985-b687-18dca6e47510"
    #     headers = {'Content-type': 'application/json'}
    #     data = {
    #         "msgtype": "text",
    #         "text": {
    #             "content": f"UI自动化用例执行结果，请点击下方链接：\n {report_link}",
    #             "mentioned_mobile_list": [],
    #         }
    #     }
    #     requests.post(url=robot_url, headers=headers, json=data).json()
