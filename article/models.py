# coding:utf-8

from django.db import models

# Create your models here.

# reporter belongs to article
class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        # 會出現在後檯的 List String
        return self.first_name+' '+self.last_name

    pass

# the article maye have many reporter
class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()

    # 會產生一個 reporter_id 的欄位
    reporter = models.ForeignKey(Reporter,related_name='reporters')

    def __unicode__(self):
        # 會出現在後檯的 List String
        return self.headline
    pass