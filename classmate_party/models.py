# -*- coding: utf-8 -*-

from django.db import models


class Person(models.Model):

    ACTIVITY_1 = 'activity_1'
    ACTIVITY_2 = 'activity_2'
    HOTEL_56 = 'hotel_56'
    HOTEL_57 = 'hotel_57'

    CATEGORY_CHOICE = (
        (ACTIVITY_1, u'活动一'),
        (ACTIVITY_2, u'活动二'),
        (HOTEL_56, u'5月6日住宿'),
        (HOTEL_57, u'5月7日住宿'),
    )

    category = models.CharField(max_length=64, choices=CATEGORY_CHOICE)
    name = models.CharField(max_length=64, blank=True, null=True)
    phone_num = models.CharField(max_length=64, blank=True, null=True)
    open_id = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    pic_url = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True)
    extra = models.TextField(blank=True, null=True)



