from django.db import models

# Create your models here.

from module.models import ModuleInfo
from product.models import ProductInfo

class UserInfo(models.Model):
    """用户信息"""
    username=models.CharField(verbose_name='用户名',max_length=20,unique=True,null=False)
    password=models.CharField(verbose_name='密码',max_length=20,null=False)
    email=models.EmailField(verbose_name='邮箱')
    status=models.BooleanField(verbose_name='有效',default=1)
    createtime=models.DateTimeField(verbose_name='创建时间',auto_now=True)

    def __str__(self):
        return self.username


class ApiInfo(models.Model):
    """接口信息"""
    module_id=models.ForeignKey(ModuleInfo,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE,null=True)
    interface_name=models.CharField('接口名称',max_length=50,null=False)
    interface_url=models.CharField('接口地址',max_length=100,null=False)
    interface_method=models.CharField('请求方法',choices=(('get','get'),('post','post'),('put','put'),('patch','patch'),('delete','delete')),default='get',max_length=20)
    interface_param=models.CharField('请求参数',max_length=200,null=True)
    interface_others=models.CharField('其他信息',max_length=100,null=True)
    create_time=models.DateTimeField('创建时间',auto_now=True)

    def __str__(self):
        return self.interface_name

    class Meta:
        verbose_name='接口信息'
        verbose_name_plural='接口信息管理'


class ApicaseInfo(models.Model):
    """接口用例信息"""
    api_id=models.ForeignKey(ApiInfo,on_delete=models.CASCADE,null=True)
    module_id=models.ForeignKey(ModuleInfo,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE,null=True)

    apicase_name=models.CharField('用例名称',max_length=50)
    apicase_desc=models.CharField('用例描述',max_length=100,null=True)
    apicase_url=models.CharField('请求地址',max_length=100)
    apicase_method=models.CharField('请求方式',choices=(('get','get'),('post','post'),('put','put'),('patch','patch'),('delete','delete')),default='get',max_length=20)
    apicase_head=models.CharField('请求头信息',max_length=100,null=True)
    apicase_param=models.CharField('请求参数',max_length=200,null=True)
    apicase_relydata=models.CharField('依赖数据',max_length=100,null=True)
    apicase_execute=models.BooleanField('是否执行',default=1)
    apicase_response=models.CharField('响应数据',max_length=300,null=True,default='')
    apicase_assert=models.CharField('断言',max_length=50,null=True)
    apicase_result=models.BooleanField('执行结果',default=0,null=True)
    apicase_needstore=models.CharField('需要存储',max_length=100,null=True)
    # apicase_storedata=models.CharField('存储数据',max_length=100,null=True,default='')
    storedata = models.CharField('存储数据', max_length=200, null=True, default='')
    apicase_taketime=models.CharField('执行耗时',max_length=20,null=True,default='')
    apicase_others=models.CharField('其他信息',max_length=100,null=True)
    execute_time=models.DateTimeField('执行时间',auto_now=True,null=True)
    create_time=models.DateTimeField('创建时间',auto_now=True)

    def __str__(self):
        return self.apicase_name

    class Meta:
        verbose_name='接口用例'
        verbose_name_plural='接口用例管理'


class ApisInfo(models.Model):
    """流程接口信息"""
    module_id=models.ForeignKey(ModuleInfo,on_delete=models.CASCADE,null=True,default='')
    product_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE,null=True,default='')
    case_id = models.ForeignKey(ApicaseInfo,on_delete=models.CASCADE, null=True,default='')
    name=models.CharField('流程名称',max_length=50,null=False)
    desc=models.CharField('描述',max_length=100,null=True)
    execute=models.BooleanField('是否执行',default=1)
    executecase=models.CharField('已选用例',max_length=100,null=True)
    others=models.CharField('其他信息',max_length=100,null=True)
    create_time=models.DateTimeField('创建时间',auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='流程接口'
        verbose_name_plural='流程接口管理'



