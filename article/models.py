# coding:utf-8

from django.db import models

# Create your models here.

# reporter hasMany articles
class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        # 會出現在後檯的 List String
        return self.first_name+' '+self.last_name

    pass

# articles belongsTo reporter
class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()

    # 會產生一個 reporter_id 的欄位, 如果定義名稱是 repoter 就會找 reporter_id, 如果是 reporters 就會找 reporters_id
    # oneToMany, 就是 belongs_to, Reporter 會增加一個 article_set 的屬性
    reporter = models.ForeignKey(Reporter,db_column='reporter_id')

    def __unicode__(self):
        # 會出現在後檯的 List String
        return self.headline
    pass