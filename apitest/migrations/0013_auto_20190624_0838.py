# Generated by Django 2.1.3 on 2019-06-24 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0012_apisinfo_executecases'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apisinfo',
            name='caseids',
        ),
        migrations.AddField(
            model_name='apisinfo',
            name='case_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apitest.ApicaseInfo'),
        ),
        migrations.AlterField(
            model_name='apisinfo',
            name='executecases',
            field=models.CharField(max_length=100, null=True, verbose_name='已选用例'),
        ),
    ]
