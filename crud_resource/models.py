# coding:utf-8

from django.db import models

# Create your models here.
class theA(models.Model):
    a = models.AutoField(primary_key=True, db_column='theA_id')
    label = models.CharField(max_length=200)

class theB(models.Model):
    b = models.AutoField(primary_key=True, db_column='theB_id')
    label = models.CharField(max_length=200)
    a = models.ForeignKey('theA', db_column='theA_id', to_field='a')
