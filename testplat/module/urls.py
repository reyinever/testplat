from django.urls import path
from module import views

urlpatterns=[
    path('index/',views.module_index),  # 模块列表

    path('add/',views.module_add),  # 模块新增页面
    path('add_check/',views.add_check),  # 新增模块验证

    path('get_product_names/',views.get_product_names),  # 获取所有产品的名称

    path('search/',views.module_search),  # 模块查找

    path('detail/<int:mid>/',views.module_detail),  # 模块详情

    path('change/<int:mid>/',views.module_change),  # 模块修改
    path('change_check/',views.change_check),  # 修改验证

    path('delete/',views.module_delete),  # 删除模块




]