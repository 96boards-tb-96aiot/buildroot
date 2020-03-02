# -*- coding=utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser,models.Model):
    user_register_time = models.DateTimeField('date to register',auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=False, auto_now_add=True)
    isbackup = models.CharField(max_length=300,default='no')
    avatar = models.CharField(max_length=200,default='avatar-default.jpg')

class FactoryData(models.Model):
    modelname = "TestResult"
    npuresult = models.CharField(max_length=300,default='None')
    usbresult = models.CharField(max_length=300,default='None')
    ddrresult = models.CharField(max_length=300,default='None')
    stressresult = models.CharField(max_length=300,default='None')