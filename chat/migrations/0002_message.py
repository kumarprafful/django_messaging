# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-30 07:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('message', models.TextField(max_length=1024)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Room')),
            ],
        ),
    ]