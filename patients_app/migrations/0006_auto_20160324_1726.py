# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients_app', '0005_auto_20160324_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]