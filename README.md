# ProxyPool
  代理ip池
  关键词：爬虫、python、flask、蘑菇代理
  开启服务：[nohup] python app.py [&]
  以下请求为get方法：
  http://192.168.10.212:10008/get_proxy?count=10
  获取10个代理，用户独占

  http://192.168.10.212:10008/update_pool
  更新代理池，获取并放入redis默认数量的代理(默认为1)

  http://192.168.10.212:10008/modify_proxy_count?count=5
  修改代理池默认数量，改为5

  http://192.168.10.212:10008/auto_update
  请求第一次：自动更新代理池，每2秒请求一次，以默认数量为标准，缺几个填入几个
  请求第二次：关闭自动更新代理池
