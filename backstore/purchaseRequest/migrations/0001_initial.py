# Generated by Django 2.2.5 on 2020-01-07 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pr_iden', models.CharField(max_length=15, verbose_name='请购单编号')),
                ('pr_serial', models.CharField(max_length=4, verbose_name='请购单流水')),
                ('pr_type', models.CharField(max_length=20, verbose_name='需求类型')),
                ('pr_department', models.CharField(max_length=20, verbose_name='请购部门')),
                ('pr_date', models.DateTimeField(auto_now_add=True, verbose_name='请购日期')),
                ('pr_remarks', models.TextField(max_length=400, null=True, verbose_name='请购备注')),
                ('pr_status', models.IntegerField(choices=[(0, '草稿'), (1, '已审批'), (2, '已关闭')], verbose_name='请购状态')),
                ('pr_creator', models.CharField(max_length=20, verbose_name='请购创建者')),
                ('pr_createDate', models.DateTimeField(auto_now_add=True, verbose_name='请购创建时间')),
                ('pr_closer', models.CharField(max_length=20, null=True, verbose_name='请购关闭者')),
                ('pr_closer_iden', models.CharField(max_length=20, null=True, verbose_name='请购关闭者工号')),
                ('pr_closeDate', models.DateTimeField(auto_now_add=True, null=True, verbose_name='请购关闭时间')),
                ('pr_closeReason', models.TextField(max_length=200, null=True, verbose_name='请购关闭原因')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orga_pr', to='base.Organization', verbose_name='组织')),
            ],
            options={
                'verbose_name': '请购单',
            },
        ),
        migrations.CreateModel(
            name='PrDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('prd_num', models.IntegerField(verbose_name='请购数量')),
                ('prd_present_num', models.IntegerField(verbose_name='现存量')),
                ('prd_remarks', models.TextField(max_length=400, null=True, verbose_name='物料请购备注')),
                ('prd_used', models.IntegerField(choices=[(0, '未使用'), (1, '已使用')], verbose_name='明细单是否使用')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_prd', to='base.Material', verbose_name='物料')),
                ('purchase_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pr_prd', to='purchaseRequest.PurchaseRequest', verbose_name='请购单')),
            ],
            options={
                'verbose_name': '请购单物料明细',
            },
        ),
    ]
