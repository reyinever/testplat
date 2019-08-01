import re
from commont.Log import *
from commont.dict_find import dict_get
from commont.create_data import get_unique_number
import copy
from apitest.models import ApicaseInfo
from commont.encrypt import md5_encrypt
from datetime import datetime
from bug.models import Bug
from report.models import Report

"""
执行接口测试用例所需要的数据处理函数
"""


def get_assert_result(assert_data,result):
    """
    断言响应结果
    参数支持：全是字典或全是字符串
    """
    try:
        # 如果是字典类型，遍历字典查找
        if isinstance(assert_data,dict) and isinstance(result,dict):
            # 要匹配的key的个数
            num = len(assert_data.keys())
            # 记录已匹配成功的key的个数
            i = 0
            for k,v in assert_data.items():
                get_v=dict_get(result,k)
                if get_v==v:
                    i+=1
                else:
                    info('断言结果：%s，断言数据：%s，响应数据：%s' % (False, assert_data, result))
                    return False
            if i==num:
                info('断言结果：%s，断言数据：%s，响应数据：%s' % (True, assert_data, result))
                return True
            else:
                info('断言结果：%s，断言数据：%s，响应数据：%s' % (False, assert_data, result))
                return False
        else:
            # 如果是字符串用正则匹配
            reg_res=re.search(r'%s'%assert_data,result)
            if reg_res:
                info('断言结果：%s，断言数据：%s，响应数据：%s' % (True, assert_data, result))
                return True
            else:
                info('断言结果：%s，断言数据：%s，响应数据：%s' % (False, assert_data, result))
                return False

    except Exception as e:
        info('断言数据异常,断言数据：%s，响应数据：%s，异常：%s'%(assert_data,result,e))
        return None


def get_store_data(needstore_data,request_data=None,response_data=None):
    """
    存储需要存储的数据
    数据存储的格式是字典
    needstore_data 格式如：{'request':['username','password'],'response':['code','token']}
    store_data 格式如：{'request':{'username':'name','password':'pswd'},'response':{'code':'00','token':'tkn'}}
    """

    store_dt={}
    try:
        if isinstance(needstore_data,dict):
            for key,value in needstore_data.items():
                if key=='request':
                    # 要存储的数据来自请求数据
                    if isinstance(request_data,dict):
                        for k in value:
                            v=dict_get(request_data,k)
                            if v:
                                # 如果存储的是密码，需要存加密后的密码
                                if k=='password':
                                    v=md5_encrypt(v)
                                # store_dt['request'] 数据结构已存在
                                if 'request' in store_dt:
                                    store_dt['request'][k]=v
                                else:
                                    # store_dt['request'] 数据结构不存在
                                    store_dt['request']={k:v}
                            else:
                                info('需要存储的数据不存在，需要存储的数据：%s，请求数据：%s'%(needstore_data,request_data))
                    else:
                        info('请求数据不是字典类型，请求数据：%s'%request_data)
                elif key=='response':
                    # 要存储的数据来自响应数据
                    if isinstance(response_data, dict):
                        for k in value:
                            v = dict_get(response_data, k)
                            # print('v:',v)
                            if v:
                                # store_dt['response'] 数据结构已存在
                                if 'response' in store_dt:
                                    store_dt['response'][k] = v
                                else:
                                    # store_dt['response'] 数据结构不存在
                                    store_dt['response'] = {k:v}
                            else:
                                # 字典里包含有数组
                                for i in response_data.values():
                                    if isinstance(i,list):
                                        for j in i:
                                            if isinstance(j,dict):
                                                r=j.get(k)
                                                if r:
                                                    if 'response' in store_dt:
                                                        store_dt['response'][k] = r
                                                    else:
                                                        # store_dt['response'] 数据结构不存在
                                                        store_dt['response'] = {k: r}

                                info('需要存储的数据不存在，需要存储的数据：%s，响应数据：%s' % (needstore_data, response_data))
                    else:
                        info('响应数据不是字典类型，响应数据：%s'%response_data)
                else:
                    info('要存储的数据来源不存在，要存储的数据：%s')
                    return None
        else:
            info('获取存储数据失败，要存储的数据格式必须是字典类型，要存储的数据')
            return None
        if store_dt:
            return store_dt
        else:
            return None
    except Exception as e:
        info('获取存储数据异常，要存储的数据：%s，请求数据：%s，响应数据：%s'%(needstore_data,request_data,response_data))
        return None


def request_data_handler(request_data,tabObj=ApicaseInfo):
    """
    获取依赖数据
    请求数据的格式
    """
    try:
        tmp=copy.copy(request_data)
        if re.search(r'\$\{unique_number\}',tmp):
            unique_num=get_unique_number()
            tmp=re.sub(r'\$\{unique_number\}',str(unique_num),tmp)
        if re.search(r'\$\{.*?\}',tmp):
            all=re.findall(r'\$\{(.*?)\}',tmp)
            print(all)
            for item in all:
                i=item.split('->')
                instead_item=eval(tabObj.objects.get(id=int(i[1])).storedata).get(i[2]).get(i[3])
                info('要替换的数据来源：%s，数据：%s'%(item,instead_item))
                tmp=re.sub(r'\$\{%s\}'%item,'%s'%instead_item,tmp)

        info('请求数据处理成功，请求数据：%s，处理后的请求数据：%s'%(request_data,tmp))
        return tmp
    except Exception as e:
        info('处理请求数据异常，请求数据：%s'%request_data)


def write_result(caseid,response='',result='',storedata='',taketime='',tabObj=ApicaseInfo):
    try:
        caseObj=tabObj.objects.get(id=caseid)
        prefix=str(tabObj)[:-4]
        #caseObj.apicase_response=response
        caseObj.apicase_result=result
        caseObj.storedata=storedata
        caseObj.apicase_taketime=taketime[:7]
        caseObj.execute_time=datetime.now()
        caseObj.save()
        info('保存结果成功! 用例id：%s，响应数据：%s，执行结果：%s，存储数据：%s，执行耗时：%s'%(caseid,response,result,storedata,taketime))
    except Exception as e:
        info('保存结果异常！用例id：%s，响应数据：%s，执行结果：%s，存储数据：%s，执行耗时：%s\n异常：%s'%(caseid,response,result,storedata,taketime,e))


def write_bug(pid='',mid='',name='',detail='',tabObj=Bug):
    try:
        tabObj.objects.create(product_id=pid,
                              module_id=mid,
                              name=name,
                              detail=detail,
                              create_time=datetime.now()
                              )
    except Exception as e:
        info('写bug异常：%s'%e)


def write_report(pid='',mid='',name='',desc='',total=0,success=0,fail=0,detail='',tabObj=Report):
    try:
        Report.objects.create(product_id=pid,
                              module_id=mid,
                              name=name,
                              desc=desc,
                              total=total,
                              success=success,
                              fail=fail,
                              detail=detail,
                              create_time=datetime.now()
                              )

    except Exception as e:
        info('写报告异常：%s'%e)




