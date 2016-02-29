# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response

from classmate_party.decorators import need_wechat_oauth_login_if_open_in_wechat

from models import *


def index(request):
    return render_to_response('index.html', locals())


def join(request, category):
    msg = ''

    category_display = dict(Person.CATEGORY_CHOICE).get(category)

    title = u'报名 %s' % category_display

    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            msg = u'请填写姓名'
        else:
            phone_num = request.POST.get('phone_num')
            if Person.objects.filter(category=category, name=name).exists():
                msg = u'请勿重复报名'
            else:
                person = Person()
                person.category = category
                person.name = name
                person.phone_num = phone_num
                person.save()
                msg = u'报名成功,谢谢~'

    return render_to_response('join.html', locals())


def list_persons(request):

    rs = []

    for category, category_display in Person.CATEGORY_CHOICE:
        r = {}
        r['category_display'] = category_display
        r['persons'] = Person.objects.filter(category=category).order_by('update_time')
        r['count'] = r['persons'].count()
        rs.append(r)

    return render_to_response('list_persons.html', locals())


