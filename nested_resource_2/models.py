# coding:utf-8

from django.db import models

# Create your models here.


class theA(models.Model):
    # 欄位
    # 經過 resource base_url 轉換到這
    # (?P<resource_name>%s)/(?P<%s>.*?)/theA_resource2/(?P<a__a>.*?), a__a => a 剛好就是 primary_key
    a = models.AutoField(primary_key=True, db_column='theA_id')
    label = models.CharField(max_length=200)

class theB(models.Model):
    # 
    # 注意：將替被關聯的 package models 增加一個 product_set 屬性
    b = models.AutoField(primary_key=True, db_column='theB_id')
    a = models.ForeignKey('theA', db_column='theA_id', to_field='a')

class theC(models.Model):
    # 欄位
    c = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200)

class theD(models.Model):
    # 
    # 注意：將替被關聯的 package models 增加一個 product_set 屬性
    d = models.AutoField(primary_key=True)
    c = models.ManyToManyField('theC')

class theE(models.Model):
    e = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200)
    fd = models.FileField(upload_to='theE_model')

class theF(models.Model):
    f = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200)
    e = models.ForeignKey('theE')

class theG(models.Model):
    g = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200)

