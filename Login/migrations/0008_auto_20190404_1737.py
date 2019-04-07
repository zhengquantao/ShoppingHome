# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-04 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0007_chat_who_send'),
    ]

    operations = [
        migrations.CreateModel(
            name='AComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=64, null=True, unique=True)),
                ('cComment', models.CharField(default='', max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dComment', models.CharField(max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('number', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.ClassList', to_field='l_number')),
                ('uname', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.UserInfo', to_field='name')),
            ],
        ),
        migrations.AddField(
            model_name='acomment',
            name='cname',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.CComment', to_field='cname'),
        ),
        migrations.AddField(
            model_name='acomment',
            name='uname',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.MComment'),
        ),
    ]
