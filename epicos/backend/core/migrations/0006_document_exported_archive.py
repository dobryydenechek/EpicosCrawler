# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-03 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190702_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='exported_archive',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Export'),
        ),
    ]