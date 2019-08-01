from apitest.models import ApisInfo,ApicaseInfo
import time
from commont.api_request import api_request
from commont.Log import *
from commont.html_report import report_html
import os
from commont.public_var import html_report_path

from apitest.apicase_utils import (
    request_data_handler,
    get_assert_result,
    write_bug,
    write_result,
    get_store_data,
    write_report,
)


def run_apis(apisTabObj=ApisInfo,caseTabObj=ApicaseInfo):
    """获取流程中选择的用例名称"""
    # 获取要执行的流程
    apiss=apisTabObj.objects.filter(execute=True)
    for apis in apiss:
        # 流程名称
        apis_name=apis.name
        # 获取每个流程中要执行的用例（对象）
        caseObj_list=[]
        if apis.executecase:
            try:
                # 获取要执行的用例名称
                execute_case_names=apis.executecase.strip().split('、')
                for execute_case_name in execute_case_names:
                    # 根据用例名称找到用例记录
                    caseObj=caseTabObj.objects.filter(apicase_name=execute_case_name)
                    if len(caseObj)>0:
                        for case in caseObj:
                            caseObj_list.append(case)
                    else:
                        info('不存在用例名称：%s ，流程名称：%s'%(execute_case_name,apis_name))
            except Exception as e:
                info('用例名称：%s ,找用例异常：%s'%(execute_case_name,e))
        if caseObj_list:
            run_cases(caseObj_list,report_name_middle=apis_name,report_desc='自动化测试流程接口')
        else:
            info('流程名称：%s，无可执行的用例'%apis_name)


def run_cases(caseObj_list,report_name_middle='流程接口测试报告',report_desc=''):
    """执行用例"""
    # 要执行的用例
    # print('caseObj_list:',caseObj_list)
    # 用例总数
    total=len(caseObj_list)
    # 记录成功用例数
    success=0
    # 记录失败用例数
    fail=0
    # 保存执行结果
    total_data=[]
    # 执行用例
    for case in caseObj_list:
        # print('case:',case)
        pid=case.product_id
        mid=case.module_id
        id=case.id
        casename=case.apicase_name
        url=case.apicase_url
        method=case.apicase_method
        head=case.apicase_head
        requestdata=case.apicase_param
        assertdata=case.apicase_assert
        needstore=case.apicase_needstore

        # 处理请求数据
        if '$' in requestdata:
            requestdata=request_data_handler(requestdata,tabObj=ApicaseInfo)
            print('请求数据：',requestdata)
        # 计时开始
        start_time=time.time()
        # 发请求
        res=api_request(url,method,eval(requestdata))
        # 耗时
        take_time=time.time()-start_time
        print(res.json())
        # 响应成功
        if res.status_code==200:
            # 断言
            if assertdata:
                assert_result=get_assert_result(eval(assertdata),res.json())
                print('断言结果：',assert_result)
            else:
                assert_result=''
            # 存储数据
            if needstore:
                store_data=get_store_data(eval(needstore),eval(requestdata),res.json())
                print('存储数据：',store_data)
            else:
                store_data=''
            # 写执行结果
            write_result(id,response=res.text[:50],result=assert_result,storedata='%s'%store_data,taketime='%s'%take_time,tabObj=ApicaseInfo)
            # 写bug
            if not assert_result:
                fail+=1
                bugname='%s，测试失败'%casename
                # detail='用例id：%s,请求地址：%s,请求方法：%s,请求数据：%s，响应结果：%s，断言：%s'%(id,url,method,requestdata,res.text[:50],assertdata)
                detail = '用例id：%s,请求数据：%s，响应结果：%s，断言：%s' % (id, requestdata, res.text[:10], assertdata)
                write_bug(pid=pid,mid=mid,name=bugname,detail=detail)
                total_data.append([url,requestdata,res.text,take_time,assertdata,'失败'])
            else:
                success+=1
                total_data.append([url, requestdata, res.text[:50], take_time, assertdata, '成功'])
        # 响应失败
        else:
            info('响应失败，响应码：%s,结果：%s'%(res.status_code,res.text))
        info('-'*50)

    # 写报告
    name=report_name_middle
    desc=report_desc
    file_name=time.strftime('%Y-%m-%d_%H-%M-%S')+name+'测试报告'
    file_path=os.path.join(html_report_path,file_name)
    # 保存测试到html文件
    report_html(total_data,file_path)
    detail=file_name
    write_report(pid=pid,mid=mid,name=name,desc=desc,total=total,success=success,fail=fail,detail=detail)


if __name__ == '__main__':
    print(run_apis())

