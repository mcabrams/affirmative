# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confirm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmation',
            name='dst_path',
            field=models.FilePathField(allow_files=False, allow_folders=True, default='foo', path='/Volumes', recursive=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='confirmation',
            name='src_path',
            field=models.FilePathField(allow_folders=True, default='foo', path='/Volumes', recursive=True),
            preserve_default=False,
        ),
    ]
