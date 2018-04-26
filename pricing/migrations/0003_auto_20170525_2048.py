# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 20:48
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0002_pricedebayitems'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PricedEbayItems',
        ),
        migrations.AddField(
            model_name='ebay139971',
            name='priced',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ebay139971',
            name='purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ebay139971',
            name='ASINInfo',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True),
        ),
    ]
