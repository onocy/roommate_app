# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-03 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doma', '0013_remove_profile_presence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='deadline',
            field=models.DateTimeField(help_text='When is this chore due?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='deadline',
            field=models.DateTimeField(help_text='When is this event going to occur?'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='deadline',
            field=models.DateTimeField(help_text='When is this reminder due?'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='deadline',
            field=models.DateTimeField(help_text='When is this transaction due?'),
        ),
    ]
