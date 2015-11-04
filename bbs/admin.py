#-*- coding:utf-8 -*-
from django.contrib import admin
from .models import Board, Post, Reply, UserAddon
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class post_admin(SummernoteModelAdmin):
    list_display = ('post_title', 'post_parent', 'post_date')
    search_fields = ('post_title',)
    list_filter = ('post_parent',)
    ordering = ('-post_date',)


class board_admin(SummernoteModelAdmin):
    list_display = ('board_name', 'board_parent')


class reply_admin(SummernoteModelAdmin):
    list_display = ('reply_title', 'reply_parent', 'reply_date')
    list_filter = ('reply_parent',)
    ordering = ('-reply_date',)


admin.site.register(Board, board_admin)
admin.site.register(Post, post_admin)
admin.site.register(Reply, reply_admin)
admin.site.register(UserAddon)