"""testplat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('apitest/',include('apitest.urls')),   # 包含应用 apitest 中的urls文件

    path('product/',include('product.urls')),  # 产品管理

    path('module/',include('module.urls')),  # 模块管理

    path('bug/',include('bug.urls')),  # bug管理

    path('report/',include('report.urls'))  # 报告管理


]
