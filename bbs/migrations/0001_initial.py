# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('board_name', models.CharField(verbose_name='版块名称', max_length=100)),
                ('board_info', models.TextField(verbose_name='版块说明', blank=True, null=True)),
                ('board_manager', models.ManyToManyField(verbose_name='版主', default='暂缺', blank=True, to=settings.AUTH_USER_MODEL)),
                ('board_parent', models.ForeignKey(verbose_name='父版块', to='bbs.Board', blank=True, null=True)),
            ],
            options={
                'verbose_name': '版面分类',
                'verbose_name_plural': '版面分类',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('post_title', models.CharField(verbose_name='主题标题', max_length=500)),
                ('post_attach', models.FileField(upload_to='files', verbose_name='附件', null=True, blank=True)),
                ('post_istop', models.BooleanField(verbose_name='置顶', default=False)),
                ('post_content', models.TextField(verbose_name='主题内容')),
                ('post_date', models.DateTimeField(verbose_name='发布时间')),
                ('post_clicks', models.IntegerField(verbose_name='阅读数', default=0)),
                ('post_parent', models.ForeignKey(verbose_name='所属版块', to='bbs.Board')),
                ('post_user', models.ForeignKey(verbose_name='发布人', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '主题',
                'ordering': ['-post_date', 'id'],
                'verbose_name_plural': '主题',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('reply_title', models.CharField(verbose_name='回复标题', max_length=500)),
                ('reply_attach', models.FileField(upload_to='files', verbose_name='附件', null=True, blank=True)),
                ('reply_content', models.TextField(verbose_name='回复内容')),
                ('reply_date', models.DateTimeField(verbose_name='回复时间')),
                ('reply_parent', models.ForeignKey(verbose_name='所属主题', to='bbs.Post')),
                ('reply_user', models.ForeignKey(verbose_name='发布人', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '回复',
                'verbose_name_plural': '回复',
            },
        ),
        migrations.CreateModel(
            name='UserAddon',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('uuid', models.CharField(verbose_name='uuid', max_length=100)),
                ('userhead', models.FileField(blank=True, null=True, upload_to='files')),
                ('sex', models.CharField(max_length=10)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
