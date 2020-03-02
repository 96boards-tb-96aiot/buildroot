# -*- coding=utf-8 -*-

from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(FactoryData)
