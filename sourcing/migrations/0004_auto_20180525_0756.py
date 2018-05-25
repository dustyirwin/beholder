# Generated by Django 2.0.4 on 2018-05-25 07:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sourcing', '0003_alibaba_amazon_ebay_walmart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('itemId', models.CharField(max_length=14)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='alibaba',
            old_name='aliId',
            new_name='alibabaId',
        ),
        migrations.RenameField(
            model_name='walmart',
            old_name='walId',
            new_name='itemId',
        ),
    ]
