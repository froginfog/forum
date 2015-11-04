# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import os
from django_summernote.widgets import SummernoteWidget


class LoginForms(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}))
    vcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))


class RegistForms(forms.Form):
    username = forms.CharField(max_length=50, min_length=2, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                          'placeholder': '填写用户名，至少2个字符',
                                                                                          'required': 'required'
                                                                                          }))
    pwd = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                          'placeholder': '密码至少8位',
                                                                          'required': 'required'
                                                                          }))
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=((u'男', '男'), (u'女', '女')))
    head = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    pwd2 = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                           'placeholder': '再次输入密码确认',
                                                                           'required': 'required'
                                                                           }))
    mail = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': '验证邮件将发往此邮箱',
                                                           'required': 'required'
                                                           }))

    def clean_username(self):
        username = self.cleaned_data['username']
        u = User.objects.filter(username=username)
        if u:
            raise forms.ValidationError(u'用户名已被注册')
        return username

    def clean_head(self):
        support = ('.jpg', '.gif', '.png')
        head = self.cleaned_data['head']
        filetype = os.path.splitext(head.name)[1].lower()
        if filetype not in support:
            raise forms.ValidationError(u'头像只支持jpg、gif、png格式')
        if head.size > 5000000:
            raise forms.ValidationError(u'图片大小不能超过5M')
        return head

    def clean_pwd2(self):
        pwd = self.cleaned_data['pwd']
        pwd2 = self.cleaned_data['pwd2']
        if pwd != pwd2:
            raise forms.ValidationError(u'两次输入密码不一样')
        return pwd2


class PostForms(forms.Form):
    post_title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'required',
    }))
    post_content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'required': 'required',
        'width': '50%',
        'height': '400px'
    }))
    post_attach = forms.FileField(required=False, widget=forms.FileInput({
        'class': 'form-control',
    }))
    vcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))

    def clean_post_attach(self):
        support = ('.zip', '.rar')
        attach = self.cleaned_data['post_attach']
        if attach:
            filetype = os.path.splitext(attach.name)[1].lower()
            if filetype not in support:
                raise forms.ValidationError(u'附件只支持zip、rar格式')
            if attach.size > 5000000:
                raise forms.ValidationError(u'附件大小不能超过%s' %attach.size)
        else:
            pass
        return attach


class SearchForms(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': u'搜索帖子',
        'required': 'required'
    }))
