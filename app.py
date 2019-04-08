from flask import Flask, request
from config import port, logger, auto_update_flag
import requests
import json
import asyncio
import threading

from proxy_class import Proxy

app = Flask(__name__)
proxy_obj = Proxy()
if auto_update_flag:
    threading.Thread(target=proxy_obj.auto_update).start()


@app.route('/get_proxy', methods=['GET'])
def get_proxy():
    addr = request.remote_addr
    ip_count = request.args.get('count')
    logger.info(addr + ' >>> ' + '请求代理数量：' + ip_count)
    resp = proxy_obj.get_proxy(ip_count)

    return json.dumps(resp, ensure_ascii=False)


@app.route('/modify_proxy_count')
def modify_ip_count():
    ip = request.remote_addr
    proxy_obj.ip_count = request.args.get('count')
    logger.info(ip + ' >>> ' + '修改IP数量:' + proxy_obj.ip_count)
    resp = {
        'isSuccess': True,
        'code': 100,
        'msg': '修改成功'
    }
    return json.dumps(resp, ensure_ascii=False)


@app.route('/update_pool')
def update_pool():
    ip = request.remote_addr

    logger.info(ip + ' >>> ' + '更新代理池')
    resp = proxy_obj.update_pool()

    return json.dumps(resp, ensure_ascii=False)


@app.route('/auto_update')
def auto_update():
    ip = request.remote_addr
    if proxy_obj.auto_update_flag:
        logger.info(ip + ' >>> ' + '关闭自动更新')
        proxy_obj.auto_update_flag = False
        resp = {
            'isSuccess': True,
            'code': 100,
            'msg': '已关闭自动更新'
        }
        return json.dumps(resp, ensure_ascii=False)
    else:
        logger.info(ip + ' >>> ' + '开启实时更新')
        proxy_obj.auto_update_flag = True
        threading.Thread(target=proxy_obj.auto_update).start()
        resp = {
            'isSuccess': True,
            'code': 100,
            'msg': '已开启自动更新'
        }
        return json.dumps(resp, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
    logger.info('服务开启')
