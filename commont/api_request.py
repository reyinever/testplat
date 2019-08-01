import requests
import json
from commont.Log import *
from commont.encrypt import md5_encrypt


def api_request(url,request_method,request_data='',headers=None,cookies=None):
    if request_method=='get':
        try:
            if isinstance(request_data,dict):
                info("请求的接口地址是：%s" % url)
                info("请求的数据是：%s" % request_data)
                r=requests.get(url,params=request_data)
            else:
                r=requests.get(url+str(request_data))
                info("请求的接口地址是：%s" % r.url)
                info("请求的数据是：%s" % request_data)
        except Exception as e:
            info("get 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" %(url,request_data,e))
            r=None
        return r
    elif request_method=="post":
        try:
            if isinstance(request_data, dict):
                info("请求的接口地址是：%s" % url)
                info("请求的数据是：%s" % json.dumps(request_data))
                r = requests.post(url, data=json.dumps(request_data))
            else:
                raise ValueError
        except ValueError as e:
            print("post 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" % (url, request_data, "请求参数不是字典类型"))
            r = None
        except Exception as e:
            print("post 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" % (url, request_data, e))
            r = None
        return r
    elif request_method=='put':
        try:
            if isinstance(request_data, dict):
                info("请求的接口地址是：%s" % url)
                info("请求的数据是：%s" % json.dumps(request_data))
                r = requests.put(url, data=json.dumps(request_data))
            else:
                raise ValueError
        except ValueError as e:
            info("put 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" % (url, request_data, "请求参数不是字典类型"))
            r = None
        except Exception as e:
            info("put 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" % (url, request_data, e))
            r = None
        return r


if __name__ == '__main__':
    uname='hahaha111111'
    pswd='123456789abc'
    pswd_encrypt=md5_encrypt(pswd)
    # 注册
    # r1 = api_request("http://39.106.41.11:8080/register/", "post",{"username": uname, "password": pswd, "email": "sed@qq.com"})
    # print(r1.json())

    # 登录
    # r2 = api_request("http://39.106.41.11:8080/login/", "post",{"username": uname, "password": pswd_encrypt})
    # print(r2.json())
    # print(type(r2))
    # token=r2.json().get('token')
    # print(token)
    # userid=r2.json().get('userid')
    # print(userid)

    # 发布博文
    token='071a336b9b9c033fb82273199b2e281f'
    userid=2590

    # r3 = api_request("http://39.106.41.11:8080/create/", "post",
    #                 {'userid': userid, 'token': token, 'title': "mysql ",
    #                  'content': 'mysql learn'})
    # print(r3.json())

    # 获取所有博客内容
    r4 = api_request("http://39.106.41.11:8080/getBlogsOfUser/", "post",
                    {'userid': userid, 'token': token})
    print(r4.json())

    # 获取单篇博客的内容
    # articleId= 46
    # r5=api_request("http://39.106.41.11:8080/getBlogContent/","get",articleId)
    # print(r5)

