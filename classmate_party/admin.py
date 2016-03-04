# -*-coding=utf-8-*-

from django.contrib import admin
from .models import Person
from .custom_model_admin import CustomModelAdmin


class PersonAdmin(CustomModelAdmin):
    list_display = ('category', 'name', 'phone_num', 'update_time', 'location')
    list_filter = ('category',)
    fields = ('category', 'name', 'phone_num', 'open_id', 'nickname',
              'location', 'pic_url', 'update_time', 'extra',
              'pic', 'rotate_picture')
    readonly_fields = ('update_time', 'pic', 'rotate_picture')

    def pic(self, obj):
        return u'<img src="%s">' % obj.pic_url

    pic.allow_tags = True
    pic.short_description = u'图片'

    def rotate_picture(self, obj):
        return u'<a href="/persons/%s/rotate_picture/">点击旋转90度</a>' % obj.id

    rotate_picture.allow_tags = True
    rotate_picture.short_description = u'旋转图片'


admin.site.register(Person, PersonAdmin)
