from django.urls import path
from apitest import views

urlpatterns=[

    path('register/',views.register),  # 注册页面
    path('register_check/',views.register_check),  # 注册验证
    path('login/',views.login),  # 登录页面
    path('login_verify_code/',views.login_verify_code),  # 产生登录验证码
    path('login_check/',views.login_check),   # 登录验证

    path('logout/',views.logout),  # 退出

    path('index/',views.index),  # 接口页面
    path('add/',views.apitest_add),  # 接口新增页面
    path('add_check/',views.apitest_add_check),  # 接口新增验证
    path('detail/<int:apiid>/',views.apitest_detail),  # 接口详情页面
    path('change/<int:apiid>/',views.apitest_change),  # 接口信息修改页面
    path('change_check/',views.apitest_change_check),  # 接口信息修改验证
    path('delete/',views.apitest_delete),  # 接口信息删除
    path('search/',views.apitest_search),  # 接口查找页面


    path('apicase/',views.apicase),  # 接口用例页面
    path('apicase/add/',views.apicase_add),  # 接口用例新增页面
    path('get_module_names/',views.get_module_names),  # 获取所有模块名称
    path('pid<int:pid>/module_names/',views.pid_module_names),  # 获取产品下的模块名称
    path('apicase/add_check/',views.apicase_add_check),  # 接口用例新增验证
    path('apicase/search/',views.apicase_search),  # 用例查找功能

    path('apicase/detail/<int:acid>/',views.apicase_detail),  # 用例详情页
    path('apicase/change/<int:acid>/',views.apicase_change),  # 用例修改页
    path('apicase/delete/',views.apicase_delete),  # 删除用例
    path('apicase/change_check/',views.apicase_change_check),  # 修改接口用例验证

    path('apicase/run/',views.run_apicases),  # 执行接口测试用例

    path('apis/',views.apis_index),  # 流程接口列表
    path('apis/add/',views.apis_add),  # 流程新增页面
    path('apis/pid<int:pid>/mid<int:mid>/case_names/',views.pid_mid_case_names),  # 获取用例名称
    path('apis/add_check/',views.apis_add_check),  # 新增流程验证
    path('apis/detail/<int:apisid>/',views.apis_detail),  # 流程详情页面
    path('apis/change/<int:apisid>/',views.apis_change),  # 流程修改页面
    path('apis/change_check/',views.apis_change_check),  # 流程修改验证
    path('apis/delete/',views.apis_delete),  # 删除流程
    path('apis/search/',views.apis_search),  # 流程名称查找

    path('apis/run/',views.apis_run),  # 执行流程接口测试


]