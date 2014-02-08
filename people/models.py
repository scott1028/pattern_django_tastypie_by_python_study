# coding:utf-8

from django.db import models

# Create your models here.
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
# from django.db import models
from django.utils.text import slugify

# Create your models here.
class people(models.Model):
    # 如果有資料庫關聯
    # user = models.ForeignKey(User)
    
    # 欄位
    create_date = models.DateTimeField(default=now)
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=200)

    # test after syncdb through south package modify database table schema...
    note = models.TextField(null=True) # set it allow null

    # 代表 people row 欄位必須強制為 unicode string
    def __unicode__(self):
        return self.name