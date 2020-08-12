# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-08-12 03:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='行政区域名')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='area.Area', verbose_name='上级行政区域')),
            ],
            options={
                'verbose_name': '行政区域',
                'verbose_name_plural': '行政区域',
                'db_table': 'tb_areas',
            },
        ),
    ]
