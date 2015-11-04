# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForms, RegistForms, PostForms, SearchForms
from .models import Board, Reply, Post, UserAddon
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models import Count, Q
from django.core.paginator import Paginator
import os
import time
import datetime
import uuid
# Create your views here.


def sendmail(who):
    u = get_object_or_404(User, username=who)
    mail_to = u.email
    a = get_object_or_404(UserAddon, user=u)
    uid = a.uuid
    link = settings.DOMAIN + '/v/' + uid
    html = '''
    此邮件来自<a herf="http://%s" target="_blank">斌之骚</a>。<br>
    这是一封激活邮件，用来激活账号或密码重置，请勿回复。<br>
    请点击或复制下面的链接到浏览器：<br>
    http://%s<br>
    此链接仅本次有效。
    ''' % (settings.DOMAIN, link)
    subject = '发给这么骚的你'
    msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [mail_to])
    msg.attach_alternative(html, 'text/html')
    msg.content_subtype = 'html'
    msg.send()



def index(req):
    board1st = Board.objects.filter(board_parent__isnull=True)
    board2nd = Board.objects.annotate(num_post=Count('post')).filter(board_parent__isnull=False)
    last_post = []
    for b in board2nd:
        try:
            last = Post.objects.filter(post_parent=b).order_by('-post_date')[0]
        except:
            last = ''
        last_post.append(last)
    c = {'board1st': board1st, 'board2nd': board2nd, 'last_post': last_post}
    return render(req, 'index.html', c)


def user_login(req):
    form = LoginForms(req.POST)
    if form.is_valid():
        form = form.cleaned_data
        username = form['username']
        pwd = form['pwd']
        if form['vcode'] != req.session['vcode']:
            return HttpResponse("<script LANGUAGE='javascript'>alert('请输入正确的验证码');history.go(-1);</script>")
        user = authenticate(username=username, password=pwd)
        if user is not None:
            if user.is_active:
                login(req, user)
                req.session['login_ok'] = 1
                req.session['user_name'] = user.username
                req.session['user_id'] = user.id
                return HttpResponseRedirect(req.GET.get('next'))
            else:
                return HttpResponseRedirect(req.GET.get('next'))
        else:
            return HttpResponse("<script LANGUAGE='javascript'>alert('用户名密码错误');history.go(-1);</script>")


def user_logout(req):
    logout(req)
    next = req.GET.get('next')
    return HttpResponseRedirect(next)


def regist(req):
    if req.method == 'POST':
        form = RegistForms(req.POST, req.FILES)
        if form.is_valid():
            form = form.cleaned_data
            username = form['username']
            pwd = form['pwd']
            sex = form['sex']
            head = req.FILES['head']
            mail = form['mail']
            user = User.objects.create_user(username, mail, pwd)
            user.is_active = False
            user.save()
            head.name = 'header-%s' % str(time.time()).replace('.', '') + os.path.splitext(head.name)[1].lower()
            uid = str(uuid.uuid1()).replace('-', '')
            s = UserAddon(sex=sex, user=user, userhead=head, uuid=uid)
            s.save()
            sendmail(username)
            return HttpResponseRedirect('/')
    else:
        form = RegistForms()
    return render(req, 'regist.html', {'form': form})


def verify(req, uid):
    try:
        useraddon = UserAddon.objects.get(uuid=uid)
        user = get_object_or_404(User, useraddon=useraddon)
        user.is_active = True
        user.save()
        useraddon.uuid = str(uuid.uuid1()).replace('-', '')
        useraddon.save()
        return HttpResponseRedirect('/')
    except:
        return HttpResponse("<script>alert('再胡搞我就要报警了！');window.location.href='http://www.cyberpolice.cn/wfjb/';</script>")


def post_list(req, bid):
    if bid:
        b2 = get_object_or_404(Board, pk=bid)
        b1 = b2.board_parent
        p_list = Post.objects.annotate(num_rep=Count('reply')).filter(post_parent=bid).order_by('-post_istop', '-post_date')
        pg = Paginator(p_list, settings.POST_PER_PAGE)
        try:
            page = int(req.GET.get('page'))
            if not page or page < 1:
                raise ValueError
        except:
            page = 1
        try:
            p_list = pg.page(page)
        except:
            p_list = pg.page(1)
        context = {'post': p_list, 'pg': pg, 'b1': b1, 'b2': b2}
        return render(req, 'list.html', context)
    else:
        return HttpResponseRedirect('/')


def show(req, pid):
    if pid:
        post = get_object_or_404(Post, id=pid)
        post.post_clicks += 1
        post.save()
        reply = Reply.objects.filter(reply_parent=post)
        pu = UserAddon.objects.get(user=post.post_user)
        ru = []
        for r in reply:
            ru.append(UserAddon.objects.get(user=r.reply_user))
        ru = list(set(ru))
        pg = Paginator(reply, settings.REPLY_PER_PAGE)
        try:
            page = int(req.GET.get('page'))
            if not page or page < 1:
                raise ValueError
        except:
            page = 1
        try:
            reply = pg.page(page)
        except:
            reply = pg.page(1)
        context = {'post': post, 'reply': reply, 'pg': pg, 'pu': pu, 'ru': ru, 'pagesize': settings.REPLY_PER_PAGE, 'thispage': page}
        return render(req, 'show.html', context)
    else:
        return HttpResponseRedirect('/')


def post(req, bid):
    if bid:
        if req.method == 'POST':
            pform = PostForms(req.POST, req.FILES)
            if pform.is_valid():
                pform = pform.cleaned_data
                if pform['vcode'] != req.session['vcode']:
                    return HttpResponse("<script LANGUAGE='javascript'>alert('请输入正确的验证码');history.go(-1);</script>")
                post_title = pform['post_title']
                post_content = pform['post_content']
                post_user_id = req.session['user_id']
                post_parent_id = bid
                post_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if 'post_attach' in req.FILES:
                    post_attach = req.FILES['post_attach']
                    post_attach.name = 'file' + str(time.time()).replace('.', '') + os.path.splitext(post_attach.name)[1].lower()
                else:
                    post_attach = ''
                try:
                    s = Post(post_title=post_title,
                             post_content=post_content,
                             post_user_id=post_user_id,
                             post_parent_id=post_parent_id,
                             post_date=post_date,
                             post_attach=post_attach
                             )
                    s.save()
                except:
                    return HttpResponseRedirect('http://www.cyberpolice.cn/wfjb/')
                return HttpResponseRedirect('/show/%d' % s.id)
        else:
            pform = PostForms()
        return render(req, 'post.html', {'pform': pform})
    else:
        return HttpResponseRedirect('/list/%d' % bid)


def reply(req, pid):
    if pid:
        p = get_object_or_404(Post, pk=pid)
        pt = p.post_title
        if req.method == 'POST':
            pform = PostForms(req.POST, req.FILES)
            if pform.is_valid():
                pform = pform.cleaned_data
                if pform['vcode'] != req.session['vcode']:
                    return HttpResponse("<script LANGUAGE='javascript'>alert('请输入正确的验证码');history.go(-1);</script>")
                reply_title = pform['post_title']
                reply_content = pform['post_content']
                reply_user_id = req.session['user_id']
                reply_parent_id = pid
                reply_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if 'post_attach' in req.FILES:
                    reply_attach = req.FILES['post_attach']
                    reply_attach.name = 'file' + str(time.time()).replace('.', '') + os.path.splitext(reply_attach.name)[1].lower()
                else:
                    reply_attach = ''
                try:
                    s = Reply(reply_title=reply_title,
                              reply_content=reply_content,
                              reply_user_id=reply_user_id,
                              reply_parent_id=reply_parent_id,
                              reply_date=reply_date,
                              reply_attach=reply_attach)
                    s.save()
                except:
                    return HttpResponseRedirect('http://www.cyberpolice.cn/wfjb/')
                return HttpResponseRedirect('/show/%s' % pid)
        else:
            pform = PostForms(initial={'post_title': 're:%s' % pt})
        return render(req, 'post.html', {'pform': pform})


def search(req):
    if req.GET.get('search'):
        keyword = req.GET.get('search')
        result = Post.objects.filter(Q(post_title__icontains=keyword) | Q(post_content__icontains=keyword)).annotate(num_rep=Count('reply')).order_by('-post_date')
        pg = Paginator(result, settings.POST_PER_PAGE)
        try:
            page = int(req.GET.get('page'))
            if not page or page < 1 or 'page' not in req.GET:
                raise ValueError
        except:
            page = 1
        try:
            result = pg.page(page)
        except:
            result = pg.page(1)
        context = {'result': result, 'pg': pg, 'search': keyword}
        return render(req, 'search.html', context)
