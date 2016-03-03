# -*-coding=utf-8-*-

from django.contrib import admin
from .models import Person
from .custom_model_admin import CustomModelAdmin

class PersonAdmin(CustomModelAdmin):
    list_display = ('category', 'name', 'phone_num', 'update_time', 'location')
    list_filter = ('category', )


admin.site.register(Person, PersonAdmin)
