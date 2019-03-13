# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-11 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doma', '0015_remove_forum_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='home',
            name='forum',
        ),
        migrations.AddField(
            model_name='forum',
            name='home',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='doma.Home'),
            preserve_default=False,
        ),
    ]
