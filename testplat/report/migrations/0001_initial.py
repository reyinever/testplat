# Generated by Django 2.1.3 on 2019-06-23 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('module', '0003_auto_20190620_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='报告名称')),
                ('desc', models.CharField(max_length=100, null=True, verbose_name='报告描述')),
                ('total', models.IntegerField(verbose_name='用例总数')),
                ('success', models.IntegerField(verbose_name='成功用例数')),
                ('fail', models.IntegerField(verbose_name='失败用例数')),
                ('detail', models.CharField(max_length=150, null=True, verbose_name='详情')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('module_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='module.ModuleInfo')),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.ProductInfo')),
            ],
            options={
                'verbose_name': 'report',
                'verbose_name_plural': '报告管理',
            },
        ),
    ]
