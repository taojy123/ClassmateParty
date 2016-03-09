# -*- coding: utf-8 -*-
import os
import uuid

from PIL import Image
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
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
        location = location1 + ' ' + location2
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

                modify_persons = []
                for category in categorys:
                    person, created = Person.objects.get_or_create(category=category, name=name)
                    modify_persons.append(person)

                for person in Person.objects.filter(name=name):
                    update_fields = ['phone_num', 'pic_url', 'location']
                    if person in modify_persons:
                        update_fields.append('update_time')
                    person.phone_num = phone_num
                    person.pic_url = pic_url
                    person.location = location
                    person.save(update_fields=update_fields)

                success = True

            except:
                msg = u'请上传一张您的近期照片'

    return render_to_response('join.html', locals())


def list_persons(request):

    rs = []

    for category, category_display in Person.CATEGORY_CHOICE:
        r = {}
        r['category_display'] = category_display
        r['persons'] = Person.objects.filter(category=category).order_by('-update_time')
        r['count'] = r['persons'].count
        rs.append(r)

    return render_to_response('list_persons.html', locals())


def rotate_picture(request, person_id):

    person = Person.objects.get(id=person_id)

    pic_path = person.pic_url.strip('/')
    im = Image.open(pic_path)
    im = im.rotate(90)
    im.save(pic_path)

    try:
        os.remove(pic_path.replace('header', 'mini'))
    except:
        pass

    return HttpResponseRedirect('/admin/classmate_party/person/%s/' % person_id)


def mini_header(request, pic_name):

    mini_path = os.path.join(os.getcwd(), 'static', 'mini', pic_name)
    pic_path = os.path.join(os.getcwd(), 'static', 'header', pic_name)

    if not os.path.exists(mini_path):
        im = Image.open(pic_path)
        w, h = im.size
        if h > 100:
            r = h / 100.0
            w = int(w / r)
            h = int(h / r)
            im = im.resize((w, h))
        im.save(mini_path)

    s = open(mini_path, "rb").read()
    response = HttpResponse(s, content_type="application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename=%s' % pic_name
    return response

