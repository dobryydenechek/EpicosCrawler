# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-02 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_spider_additional_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='spider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Spider'),
        ),
        migrations.AlterField(
            model_name='file',
            name='spider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Spider'),
        ),
    ]
