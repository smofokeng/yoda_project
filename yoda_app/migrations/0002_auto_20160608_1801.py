# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-08 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoda_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='category',
            name='view',
            field=models.IntegerField(default=0),
        ),
    ]
