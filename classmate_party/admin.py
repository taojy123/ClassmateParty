# -*-coding=utf-8-*-

from django.contrib import admin
from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')


admin.site.register(Person, PersonAdmin)
