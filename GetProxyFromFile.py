#!usr/bin/env python
#coding=utf-8

""""
##  从文件中，读取 proxy 信息

"""


import datetime
import os

BASE_PATH = '../proxy/'
READ_FILE_DAY_NUM = -3  #天
READ_FILE_NUM_MAX = 5

# # 过滤
BASE_COUNTRY_SWITCH_WHITE = False  # True
BASE_COUNTRY_SWITCH_BLACK = (not BASE_COUNTRY_SWITCH_WHITE)
BASE_COUNTRY_WHITE = ',US,IN,DE,ID,'
BASE_COUNTRY_BLACK = ',CN,HK,IR,RU,'
BASE_PORT_BLACK = ',80,8080,4145,9050,7497,'
BASE_PROXY_SPEED_DELAY_LIMIT = 8000
TEST_RESULT_PROXY_SPEED_DELAY_LIMIT = 20


class GetProxyFromFile:

    @classmethod
    def __filter(cls, proxy_str):
        li = proxy_str.split(':')
        cnt = len(li)
        slf_limit = -1
        if cnt >= 5:
            slf_limit = li[4].strip()
        if cnt >= 4:
            limit = li[3].strip()
            if slf_limit == -1:
                slf_limit = limit
        if cnt >= 3:
            country = li[2].strip()
        if cnt >= 2:
            ip = li[0].strip()
            port = li[1].strip()
        else:
            return False

        if len(ip) <= 0 or len(port) <= 0 or len(country) <= 0:
            return False
        # # 国家白名单处理
        if BASE_COUNTRY_SWITCH_WHITE and BASE_COUNTRY_WHITE.find(',' + country + ',') < 0:
            return False
        # # 国家黑名单处理
        if BASE_COUNTRY_SWITCH_BLACK and BASE_COUNTRY_BLACK.find(',' + country + ',') >= 0:
            return False
        # # port 位数限制 5位
        # if len(port) < 5: continue
        if BASE_PORT_BLACK.find(',' + port + ',') >= 0:
            return False
        #更新时间
        if int(limit) > BASE_PROXY_SPEED_DELAY_LIMIT:
            return False
        if int(slf_limit) > TEST_RESULT_PROXY_SPEED_DELAY_LIMIT:
            return False
        return True

    # def __parse_data(self, html):
    #     pass

    def get_data(self):
        proxy_list = GetProxyFromFile.__file_load()
        proxy_list = GetProxyFromFile.__do_filter(proxy_list)
        proxy_list = GetProxyFromFile.__do_diff(proxy_list)
        return proxy_list

    @classmethod
    def __file_load(cls):
        proxy_list = []
        i = 0
        if os.path.isdir(BASE_PATH):
            children = sorted(os.listdir(BASE_PATH), reverse=True)
            limited_date_string = GetProxyFromFile.__get_date_time_str(READ_FILE_DAY_NUM)  # 取截止日期
            for child in children:
                tmp = os.path.join(BASE_PATH, child)
                if os.path.isdir(tmp):
                    pass
                else:  # elif os.path.isfile(tmp):
                    if child.startswith('spider-'):
                        # if child.startswith('spider-'):
                        if i > READ_FILE_NUM_MAX and GetProxyFromFile.__get_date_time_flag(child) < limited_date_string:  # 取最近2周的文件且数量不得小于20。
                            break
                        # logger.info(child)
                        i += 1
                        file = open(tmp, 'r')
                        try:
                            text_lines = file.readlines()
                            if len(text_lines) > 0 and len(text_lines[0]) > 10:     # 文件得有一行正确的数据
                                if len(proxy_list) == 0:
                                    proxy_list = text_lines
                                else:
                                    proxy_list.extend(text_lines)
                        finally:
                            file.close()
        return list(set(proxy_list))

    @classmethod
    def __get_date_time_str(cls, x):
        now_time = datetime.datetime.now()
        return (now_time + datetime.timedelta(days=x)).strftime('%Y%m%d')+'000000'

    @classmethod
    def __get_date_time_flag(cls, file_name):
        date_time = ''
        li = file_name.split('-')
        if len(li) >= 1:
            xxx = li[len(li)-1]
            if len(xxx) == 18 and xxx[-4:].lower() == '.txt':
                date_time = xxx[:-4]
        return date_time

    # #过滤器
    @classmethod
    def __do_filter(cls, proxy_list):
        ret_proxy_list = []
        for proxy in proxy_list:
            if GetProxyFromFile.__filter(proxy):
                ret_proxy_list.append(proxy)
        return ret_proxy_list


    # #剔重器
    @classmethod
    def __do_diff(cls, proxy_list):
        proxy_dic = {}
        for proxy in proxy_list:
            li = proxy.strip().split(':')
            cnt = len(li)
            if cnt >= 2:
                ip = li[0].strip()
                port = li[1].strip()
            else:
                continue
            key = '%s:%s' % (ip, port)
            proxy_dic[key] = proxy.strip()
        ret_proxy = []
        if(len(proxy_dic)) > 0:
            ret_proxy = proxy_dic.values()
        return ret_proxy

#
# if __name__ == '__main__':
#     spider = GetProxyFromFile()
#     proxy_list = spider.get_data()
#     print(len(proxy_list))
#     print(proxy_list)


