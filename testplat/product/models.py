from django.db import models

# Create your models here.


class ProductInfo(models.Model):
    """产品信息"""
    product_name = models.CharField('产品名称', max_length=50,unique=True,null=False)
    product_desc = models.CharField('产品描述', max_length=100, null=True)
    product_manager = models.CharField('产品负责人', max_length=20, null=False)
    product_others=models.CharField('其他信息',max_length=200,null=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        verbose_name = '产品信息'  # 增加后面展示的内容
        verbose_name_plural = '产品管理'  # 列表展示的内容

    def __str__(self):
        return self.product_name

