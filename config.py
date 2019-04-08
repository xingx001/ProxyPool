import logging
import sys
import time
import os
import redis


# 默认代理数量
ip_count = 1

# 蘑菇代理appKey
app_key = 'fb7d0ef415*******e347323930f928d'

# 端口
port = 10008

# 自动更新
auto_update_flag = False

# 日志管理
logger = logging.getLogger('logger')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s \n')
try:
    file_handler = logging.FileHandler(
        'logs/{}.log'.format(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))))
except:
    os.mkdir('logs')
    file_handler = logging.FileHandler(
        'logs/{}.log'.format(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

# redis
redis_config = {
    'host': '192.168.10.***',
    'port': 6379,
    'db':15,
}
pool = redis.ConnectionPool(**redis_config)
redis_handler = redis.Redis(connection_pool=pool)