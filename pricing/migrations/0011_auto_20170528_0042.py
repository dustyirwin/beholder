# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0010_auto_20170528_0035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ebay139971',
            name='endTime',
        ),
        migrations.AlterField(
            model_name='ebay139971',
            name='keywords',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
