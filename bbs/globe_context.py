# -*- coding:utf-8 -*-
from bbs.forms import LoginForms, SearchForms
from PIL import Image, ImageDraw, ImageFont
import random
import os
from django.conf import settings


def allforms(req):
    w, h = 100, 40
    font_file = 'G:/apache/Apache24/htdocs/second/static/fonts/simhei.ttf'
    fnt = ImageFont.truetype(font_file, 25)
    char_list = '少年阿咸闲仙贤鲜献纤馅掀腺斌宾发骚湿电蕉吔屎'
    chars = []
    chars_str = ''
    for i in range(4):
        chars.append(random.choice(char_list))
        chars_str = chars_str + chars[i]
    req.session['vcode'] = chars_str
    pic = Image.new('RGB', (w, h), (255, 255, 255))
    vcode_pic = ImageDraw.Draw(pic)
    for j in range(4):
        vcode_pic.text((5 + j*20, 5), chars[j], (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), fnt)
    del vcode_pic
    for x in range(w):
        for y in range(h):
            if pic.getpixel((x, y)) == (255, 255, 255):
                pic.putpixel((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    pic.save('G:/apache/Apache24/htdocs/second/static/images/vcode.jpg')
    login_forms = LoginForms()
    search_forms = SearchForms()
    context = {'login_forms': login_forms, 'search_forms': search_forms}
    return context


def islogin(req):
    if 'login_ok' in req.session and req.session['login_ok'] == 1:
        context = {'islogin': 1, 'user_name': req.session['user_name']}
    else:
        context = {'islogin': 0}
    return context
