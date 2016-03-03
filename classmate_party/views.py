# -*- coding: utf-8 -*-
import os
import uuid

from PIL import Image
from django.shortcuts import render_to_response
from models import *


def index(request):
    return render_to_response('index.html', locals())


def join(request):
    msg = ''

    category_choice = Person.CATEGORY_CHOICE

    if request.method == 'POST':
        categorys = request.POST.getlist('category')
        name = request.POST.get('name')
        phone_num = request.POST.get('phone_num')
        pic = request.FILES.get('pic')
        location1 = request.POST.get('location1', '')
        location2 = request.POST.get('location2', '')
        location = location1 + location2
        if not categorys:
            msg = u'请勾选报名项目'
        elif not name:
            msg = u'请填写姓名'
        elif not phone_num:
            msg = u'请填写手机号'
        else:
            try:
                im = Image.open(pic)
                w, h = im.size
                if h > 500:
                    r = h / 500.0
                    w = int(w / r)
                    h = int(h / r)
                    im = im.resize((w, h))
                filename = "static/header/%s.png" % uuid.uuid4()
                path = os.path.join(os.getcwd(), filename)
                im.save(path)
                pic_url = '/' + filename

                for category in categorys:
                    person, created = Person.objects.get_or_create(category=category, name=name)

                Person.objects.filter(name=name).update(
                    phone_num=phone_num,
                    pic_url=pic_url,
                    location=location
                )

                success = True

            except:
                msg = u'请上传一张您的近期照片'

    return render_to_response('join.html', locals())


def list_persons(request):

    rs = []

    for category, category_display in Person.CATEGORY_CHOICE:
        r = {}
        r['category_display'] = category_display
        r['persons'] = Person.objects.filter(category=category).order_by('update_time')
        r['count'] = r['persons'].count
        rs.append(r)

    return render_to_response('list_persons.html', locals())


