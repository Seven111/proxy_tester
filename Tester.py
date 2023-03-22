#!usr/bin/env python
#coding=utf-8

from concurrent.futures import ThreadPoolExecutor
import time
import socks

PROXY_CHECKER_POOL_SIZE = 80
CONNECT_TIME_OUT = (60+30)
SEND_RECEIVE_TIME_OUT = (1*60+20)
TEST_URL = 'www.google.com'
TEST_HTTP_GET_HEADER = 'GET / HTTP/1.1\r\nHost: %s\r\n%s%s%s%s%s%s\r\n' % (TEST_URL,
    'Connection: keep-alive\r\n',
    'Upgrade-Insecure-Requests: 1\r\n',
    'User-Agent: Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; TheWorld)\r\n',
    'Accept: text/html,application/xhtml+xml,application/xml\r\n',
    'Accept-Encoding: gzip, deflate\r\n',
    'Accept-Language: zh-CN,zh;q=0.9\r\n')


class Tester:

    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    def test_proxy(self, proxy):
        ret = (-1, proxy)
        # print("check[%s]" % proxy)
        if not (proxy and len(proxy) > 0):
            return ret
        limit = ''
        country = ''
        ip = ''
        port = ''
        in_proxy = proxy.strip()
        li = in_proxy.split(':')
        cnt = len(li)
        if cnt >= 4:
            limit = li[3].strip()
        if cnt >= 3:
            country = li[2].strip()
        if cnt >= 2:
            ip = li[0].strip()
            port = li[1].strip()
        else:
            return ret

        print('test_proxy:%s', proxy)
        begin_time = time.time()
        s = socks.socksocket()
        try:
            s.set_proxy(socks.SOCKS5, ip, int(port))
            s.settimeout(CONNECT_TIME_OUT)
            s.connect_ex((TEST_URL, 80))

            ret = (-2, proxy)
            s.settimeout(SEND_RECEIVE_TIME_OUT)
            s.sendall(bytes(TEST_HTTP_GET_HEADER, encoding='utf-8'))

            ret = (-3, proxy)
            resp = s.recv(1024)
            # print(resp)

        except socks.ProxyError as error:
            print(error)
            pass
        except socks.HTTPError as error:
            print(error)
            pass
        except socks.GeneralProxyError as error:
            print(error)
            pass
        except socks.ProxyConnectionError as error:
            print(error)
            pass
        except Exception as error:
            print(error)
            pass
        else:
            # print(resp)
            end_time = time.time()
            use_time = int(end_time - begin_time)
            diff = use_time
            sr = str(resp, encoding="utf8")
            ret = (0, '%s:%s:%s:%s:0%d' % (ip, port, country, limit, diff))
            # print(ret)
            # print("\r\n")
        finally:
            print(ret)
            s.close()
            return ret

    def run(self):
        ok_proxy_list = []
        with ThreadPoolExecutor(PROXY_CHECKER_POOL_SIZE) as executor:
            for data in executor.map(self.test_proxy, self.proxy_list):
                print("ret:%d index:%s" % (data[0], data[1]))
                if data[0] == 0 and data[1]:
                    ok_proxy_list.append(data[1])
        return ok_proxy_list

#
# if __name__ == '__main__':
#     pl = ['103.70.79.28:59166:ID:1004:01', '109.236.88.38:30283:NL:0']
#     tester = Tester(pl)
#     ok_list = tester.run()
#     print('finish')
#     print(len(ok_list))
#     print(ok_list)

