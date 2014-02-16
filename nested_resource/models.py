# coding:utf-8

from django.db import models

# Create your models here.

class theA(models.Model):
    a = models.AutoField(max_length=100, primary_key=True)
    label = models.TextField()

class theB(models.Model):
    b = models.AutoField(max_length=100, primary_key=True)
    label = models.TextField()
    a = models.ForeignKey(theA)
