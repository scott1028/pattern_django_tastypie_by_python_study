# coding:utf-8

from django.db import models

# Create your models here.
from tastypie.utils.timezone import now


class package(models.Model):
    # 欄位
    pub_date = models.DateTimeField(default=now)
    package_name = models.CharField(max_length=200)

    # 代表 title 欄位必須強制為 unicode string
    def __unicode__(self):
        return self.package_name

class product(models.Model):
	# 
	# 注意：將替被關聯的 package models 增加一個 product_set 屬性
    packages = models.ManyToManyField(package)
    
    # 欄位
    pub_date = models.DateTimeField(default=now)
    product_name = models.CharField(max_length=200)

    # 代表 title 欄位必須強制為 unicode string
    def __unicode__(self):
        return self.product_name