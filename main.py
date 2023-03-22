#!usr/bin/env python
#coding=utf-8


from GetProxyFromFile import GetProxyFromFile
from RWFile import RWFile
from Tester import Tester
import logging.config
import os

logging.config.fileConfig("./logging.conf")
logger = logging.getLogger(os.path.basename(__file__))

if __name__ == '__main__':
    # 用户参数处理

    reader = GetProxyFromFile()
    proxy_list = reader.get_data()

    if len(proxy_list) > 0:
        # logger.info(proxy_list)
        # logger.info(len(proxy_list))

        tester = Tester(proxy_list)
        ok_proxy_list = tester.run()

        if len(ok_proxy_list) > 0:
            logger.critical("########################################")
            logger.critical("Total:%d" % len(ok_proxy_list))
            ok_proxy_list.sort(key=lambda x: int(x[:x.rfind(':')][x[:x.rfind(':')].rfind(':') + 1:]))  ##倒数第二个':'分割的是时间
            for p in ok_proxy_list:
                logger.critical("\t%s" % p)
            logger.critical("############################################\n")
            RWFile.write_checked_file(ok_proxy_list)








