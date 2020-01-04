# Generated by Django 2.2.5 on 2020-01-04 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_auto_20200104_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='totalwarehouse',
            old_name='total_belong_iden',
            new_name='total_belong_center_iden',
        ),
        migrations.AddField(
            model_name='center',
            name='center_iden',
            field=models.CharField(default=1, max_length=8, verbose_name='中心编号'),
            preserve_default=False,
        ),
    ]