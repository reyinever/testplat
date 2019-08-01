from django.urls import path,re_path
from report import views


urlpatterns=[
    path('index/',views.report_index),   # 测试报告首页展示
    path('testReport/<str:filename>/',views.report_detail),  # 测试报告详情页
    path('search/',views.report_search),  # 测试报告查找页面
]