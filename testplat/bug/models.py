from django.db import models

# Create your models here.

from product.models import ProductInfo
from module.models import ModuleInfo


class Bug(models.Model):
    """bug信息表"""
    product_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE,null=True)   # 关联产品ID
    module_id=models.ForeignKey(ModuleInfo,on_delete=models.CASCADE,null=True)
    name=models.CharField('bug名称',max_length=50)
    detail=models.CharField('详情',max_length=150,null=True)
    create_time=models.DateTimeField('创建时间',auto_now=True)

    class Meta:
        verbose_name='bug'
        verbose_name_plural='bug管理'

    def __str__(self):
        return self.name


