# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-10 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='商品名称')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='商品价格')),
                ('spec', models.CharField(max_length=20, verbose_name='商品规格')),
                ('picture', models.ImageField(null=True, upload_to='static/upload/goods', verbose_name='商品图片')),
                ('isActive', models.BooleanField(default=True, verbose_name='是否上架')),
            ],
            options={
                'db_table': 'goods',
                'verbose_name_plural': '商品',
                'verbose_name': '商品',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='类型标题')),
                ('picture', models.ImageField(null=True, upload_to='static/upload/goodstype', verbose_name='类型图片')),
                ('desc', models.TextField(verbose_name='类型描述')),
            ],
            options={
                'db_table': 'goods_type',
                'verbose_name_plural': '商品类型',
                'verbose_name': '商品类型',
            },
        ),
        migrations.AddField(
            model_name='goods',
            name='goodsType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.GoodsType', verbose_name='商品类型'),
        ),
    ]
