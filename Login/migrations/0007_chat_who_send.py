# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-31 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0006_binfo_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='who_send',
            field=models.CharField(choices=[('1', '商家'), ('0', '用户')], default=0, max_length=10),
        ),
    ]
