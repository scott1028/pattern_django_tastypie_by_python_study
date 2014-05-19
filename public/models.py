# coding:utf-8

from django.db import models

class Product(models.Model):
	label = models.CharField(max_length=200)
	product_id = models.CharField(max_length=200, unique=True)

class MNO(models.Model):
	product = models.ForeignKey(Product, to_field='product_id', on_delete=models.SET_NULL, null=True, db_constraint=False)
	name = models.CharField(max_length=200)

class Unique(models.Model):
	no = models.CharField(max_length=200, unique=True)
