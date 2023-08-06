## 使用方法
支持使用`本地获取模式`和`队列获取模式`  
使用本地获取模式时会自动限速请求 `4 rep/s`
使用队列获取模式时 队列默认超时时间是`十分钟`  
  
使用教程
 ```python
# 导入包
import redis
from vbigbang_proxy_utils.proxy_utils import get_proxy_list, GetProxyType

# 创建redis conn对象
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='your_pwd', db=0)
redis_conn = redis.Redis(connection_pool=redis_pool)
   
# 获取代理列表
squid_proxy_list = get_proxy_list(kafka_topic='', kafka_username='', kafka_password='', bootstrap_servers=[], count=1,
                                  get_proxy_type=GetProxyType.LOCAL, p_key='your key', redis_conn=redis_conn)
for r in squid_proxy_list:
    print(r.name)
    print(r.city_name)
    print(r.real_ip)
```

## 更新日志
```bash
2022-11-14: zm代理只是使用省份进行区分 提取
2022-09-28: 队列模式支持设置超时未获取到代理IP后进行重新请求
2022-09-20: 支持自定义检查代理IP可用性的网址hosts节点
            避免因节点宕机导致检查错误从而影响业务进行

2022-09-17: 修复城市id处理异常的bug
     
2022-09-16: 首次上传
```
  
    

## 本地调试使用
1. 生成dist文件```python setup.py sdist```
2. 发布轮子```twine upload dist/*```
3. 参考```https://www.zywvvd.com/notes/coding/python/create-my-pip-package/create-my-pip-package/```