# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_system', '0004_experience_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='check_in',
            name='hunt',
            field=models.BooleanField(default=False),
        ),
    ]
