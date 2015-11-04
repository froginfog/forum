# -*- coding:utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag()
def floor(forloop, pagesize, thispage):
    return pagesize * (thispage - 1) + forloop