import threading
from config import ip_count, app_key, logger, redis_handler, auto_update_flag
import json
import requests
import time


class Proxy(object):
    INSTANCE = None
    lock = threading.RLock()

    def __init__(self):
        self.ip_count = ip_count
        self.proxies = {}
        self.auto_update_flag = auto_update_flag

    def __new__(cls):
        cls.lock.acquire()
        if cls.INSTANCE is None:
            cls.INSTANCE = super(Proxy, cls).__new__(cls)
        cls.lock.release()
        return cls.INSTANCE

    # 修改默认获取IP数量
    def modify_ip_count(self, num):
        self.ip_count = num

    # 解决特殊需求，单独返回若干个代理,share=False时不和其他客户端共享，独占几个代理，share=True时将代理放入redis
    def get_proxy(self, count, share=False):
        url = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey={}&count={}&expiryDate=0&format=1&newLine=2'.format(
            app_key, count)
        try:
            resp = requests.get(url)
        except:
            logger.warning('调用第三方接口失败,状态码:' + str(resp.status_code))
            return {'isSuccess': False, 'code': 109, 'msg': '调用第三方接口失败'}
        resp = json.loads(resp.text)
        if resp['code'] != '0':
            logger.warning('请求代理IP失败,响应结果:' + str(resp))
            return {'isSuccess': False, 'code': 101, 'msg': resp['msg']}
        else:
            proxy_list = []
            for r in resp['msg']:
                ip = r['ip']
                port = r['port']
                proxy_list.append(ip + ':' + port)
                if share:
                    redis_handler.sadd('proxyPool:proxyPool', ip + ':' + port)
            logger.info('请求代理IP成功,响应代理:' + str(proxy_list))
            return {'isSuccess': True, 'code': 100, 'msg': proxy_list}

    # 更新代理池，添加代理数量为默认的或用户设置的
    def update_pool(self):
        url = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey={}&count={}&expiryDate=0&format=1&newLine=2'.format(
            app_key, self.ip_count)
        try:
            resp = requests.get(url)
        except:
            logger.warning('调用第三方接口失败,状态码:' + str(resp.status_code))
            return {'isSuccess': False, 'code': 109, 'msg': '调用第三方接口失败'}
        resp = json.loads(resp.text)
        if resp['code'] != '0':
            logger.warning('请求代理IP失败,响应结果:' + str(resp))
            return {'isSuccess': False, 'code': 101, 'msg': resp['msg']}
        else:
            proxy_list = []
            for r in resp['msg']:
                ip = r['ip']
                port = r['port']
                proxy_list.append(ip + ':' + port)
                redis_handler.sadd('proxyPool:proxyPool', ip + ':' + port)
            logger.info('请求代理IP成功,响应代理:' + str(proxy_list))
            return {
                'isSuccess': True,
                'code': 100,
                'msg': proxy_list
            }

    # 自动更新，每次检查pool中proxy数量是否足够，不够则补全
    def auto_update(self):
        while True:
            if self.auto_update_flag:
                proxies_num = len(redis_handler.smembers('proxyPool:proxyPool'))
                if proxies_num < self.ip_count:
                    self.get_proxy(self.ip_count - proxies_num, share=True)
                time.sleep(2)
            else:
                break


if __name__ == '__main__':
    a = Proxy()
