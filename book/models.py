# coding:utf-8

from django.db import models

# Create your models here.
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
# from django.db import models
from django.utils.text import slugify


class first_book(models.Model):
    # 如果有資料庫關聯
    # user = models.ForeignKey(User)
    
    # 欄位
    pub_date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()

    # 代表 title 欄位必須強制為 unicode string
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:50]

        return super(first_book, self).save(*args, **kwargs)

class second_book(models.Model):
    # 如果有資料庫關聯
    # user = models.ForeignKey(User)
    
    # 欄位
    pub_date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()

    # 代表 title 欄位必須強制為 unicode string
    def __unicode__(self):
        return self.title

class third_book(models.Model):
    # 如果有資料庫關聯
    # user = models.ForeignKey(User)
    
    # 欄位
    pub_date = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()

    # 代表 title 欄位必須強制為 unicode string
    def __unicode__(self):
        return self.title