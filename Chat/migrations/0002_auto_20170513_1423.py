# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='ChatTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]