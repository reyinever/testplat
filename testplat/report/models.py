from django.db import models

# Create your models here.

from product.models import ProductInfo
from module.models import ModuleInfo


class Report(models.Model):
    """测试报告表"""
    product_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE,null=True)   # 关联产品ID
    module_id=models.ForeignKey(ModuleInfo,on_delete=models.CASCADE,null=True)
    name=models.CharField('报告名称',max_length=50)
    desc=models.CharField('报告描述',max_length=100,null=True)
    total=models.IntegerField('用例总数')
    success=models.IntegerField('成功用例数')
    fail=models.IntegerField('失败用例数')
    detail = models.CharField('详情', max_length=150, null=True)
    create_time=models.DateTimeField('创建时间',auto_now=True)

    class Meta:
        verbose_name='report'
        verbose_name_plural='报告管理'

    def __str__(self):
        return self.name

