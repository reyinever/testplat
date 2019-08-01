from django.db import models

# Create your models here.

from product.models import ProductInfo


class ModuleInfo(models.Model):
    """模块管理"""
    product_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE)
    module_name=models.CharField('模块名称',max_length=50,null=False,unique=True)
    module_desc=models.CharField('模块描述',max_length=100,null=True)
    module_dev=models.CharField('开发人员',max_length=100,null=True)
    module_tst=models.CharField('测试负责人',max_length=30,null=True)
    module_others=models.CharField('其他信息',max_length=100,null=True)
    create_time=models.DateTimeField('创建时间',auto_now=True)

    def __str__(self):
        return self.module_name

    class Meta:
        verbose_name='模块信息'
        verbose_name_plural='模块管理'