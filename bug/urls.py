from django.urls import path
from bug import views

urlpatterns=[
    path('index/',views.bug_index),  # bug列表首页
    path('search/',views.bug_search),  # bug查找页
]