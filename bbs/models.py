# -*-coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):  # 版面分类
    board_name = models.CharField(max_length=100, verbose_name='版块名称')
    board_parent = models.ForeignKey('self', verbose_name='父版块', blank=True, null=True)
    board_info = models.TextField(verbose_name='版块说明', blank=True, null=True)
    board_manager = models.ManyToManyField(User, verbose_name='版主', blank=True, default=u'暂缺')

    def __str__(self):
        return self.board_name

    class Meta:
        verbose_name = '版面分类'
        verbose_name_plural = verbose_name


class Post(models.Model):  # 主题
    post_title = models.CharField(max_length=500, verbose_name='主题标题')
    post_parent = models.ForeignKey(Board, verbose_name='所属版块')
    post_user = models.ForeignKey(User, verbose_name='发布人')
    post_attach = models.FileField(upload_to='files', verbose_name='附件', blank=True, null=True)
    post_istop = models.BooleanField(verbose_name='置顶', default=False)
    post_content = models.TextField(verbose_name='主题内容')
    post_date = models.DateTimeField(verbose_name='发布时间')
    post_clicks = models.IntegerField(verbose_name='阅读数', default=0)

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name
        ordering = ['-post_date', 'id']


class Reply(models.Model):
    reply_title = models.CharField(max_length=500, verbose_name='回复标题')
    reply_parent = models.ForeignKey(Post, verbose_name='所属主题')
    reply_attach = models.FileField(upload_to='files', verbose_name='附件', blank=True, null=True)
    reply_content = models.TextField(verbose_name='回复内容')
    reply_date = models.DateTimeField(verbose_name='回复时间')
    reply_user = models.ForeignKey(User, verbose_name='发布人')

    def __str__(self):
        return self.reply_title

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name


class UserAddon(models.Model):
    user = models.OneToOneField(User)
    uuid = models.CharField(max_length=100, verbose_name='uuid')
    userhead = models.FileField(upload_to='files', blank=True, null=True)
    sex = models.CharField(max_length=10)

