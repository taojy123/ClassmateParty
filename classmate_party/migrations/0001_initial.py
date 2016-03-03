# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=64, choices=[(b'activity_1', '\u6d3b\u52a8\u4e00'), (b'activity_2', '\u6d3b\u52a8\u4e8c'), (b'hotel_56', '5\u67086\u65e5\u4f4f\u5bbf'), (b'hotel_57', '5\u67087\u65e5\u4f4f\u5bbf')])),
                ('name', models.CharField(max_length=64, null=True, blank=True)),
                ('phone_num', models.CharField(max_length=64, null=True, blank=True)),
                ('open_id', models.CharField(max_length=255, null=True, blank=True)),
                ('nickname', models.CharField(max_length=255, null=True, blank=True)),
                ('pic_url', models.CharField(max_length=255, null=True, blank=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('extra', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
