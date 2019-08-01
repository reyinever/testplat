from django.urls import path

from product import views

urlpatterns=[
    path('index/',views.index),  # 产品列表页
    path('search/',views.product_search),  # 产品查找

    path('add/',views.product_add),  # 新增产品页
    path('add_check/',views.add_check),  # 新增产品验证

    path('detail/<int:pid>',views.product_detail),  # 查看详情页面

    path('change/<int:pid>/',views.product_change),  # 产品修改
    path('change_check/',views.change_check),  # 修改验证

    path('delete/',views.product_delete),  # 产品删除

]