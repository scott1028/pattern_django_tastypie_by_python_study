# coding:utf-8
# 參考：https://docs.djangoproject.com/en/dev/topics/db/managers/#adding-extra-manager-methods
# ModelManger 必須自己在定義一個 objects 成員在 Model Class 內才可以正常使用。
# 可以用來增加 model.objects.{ 方法定義在 ModelManger Class 下 }，必須重新定義 objects 成員。

from django.db import models

# Create your models here.
class theA(models.Model):
    a = models.CharField(max_length=100, primary_key=True)
    label = models.TextField()
    class Meta: 
        app_label = 'model_folder'
        # 參考 setting 內 install 的 app or app.path

class theB(models.Model):
    b = models.CharField(max_length=100, primary_key=True)
    label = models.TextField()
    class Meta: 
        app_label = 'model_folder'

class theC(models.Model):
    c = models.CharField(max_length=100, primary_key=True)
    label = models.TextField()
    class Meta: 
        app_label = 'model_folder'

class theD(models.Model):
    d = models.CharField(max_length=100, primary_key=True)
    label = models.TextField()

    # 注意：將會自動幫你關聯與 relation model field 同樣的資料欄位型態
    e = models.ForeignKey('theE', to_field='d_id', db_column='theE_d_id')
    class Meta: 
        app_label = 'model_folder'

class theE(models.Model):
    e = models.CharField(max_length=100, primary_key=True)
    label = models.TextField()
    d_id = models.CharField(max_length=3, unique=True)
    class Meta: 
        app_label = 'model_folder'

class theF(models.Model):
    f = models.CharField(max_length=100, primary_key=True)
    label = models.TextField()

    mno = models.CharField(max_length=3, unique=True)
    class Meta: 
        app_label = 'model_folder'
        db_table = 'theF'

class theG(models.Model):
    # 要設定為 IntegerField or AutoField 才會有 Auto increment 效果
    g = models.AutoField(max_length=100, primary_key=True)
    label = models.TextField()

    # 注意：將會自動幫你關聯與 relation model field 同樣的資料欄位型態
    mno = models.ForeignKey('theF', to_field='mno', db_column='mno')

    # 客製欄位
    custom_field = 1000

    # 客製 instance method, 可以用來客製化查詢用。
    def get_my_record(self):
        print 'search some record with the some condition then return!'
        try:
            return self.mno
        except:
            print 'can\'t find this queryset!'
            return 'None record'
    
    class Meta: 
        app_label = 'model_folder'
        db_table = 'theG'

# 以下展示 model manager 功能：
class myManager(models.Manager):
    # add a objects.method
    def test(self):
        return []

class person(models.Manager):
    # cumstom the field return QuerySet
    def get_queryset(self):
        # 相當於底下 person = person() 的預設 return QuerySet
        # 可以在這邊寫 model 關聯查詢
        import pdb;pdb.set()
        return [1,2,3,4]

    def authors(self):
        return 1

    def editors(self):
        return 2

class theH(models.Model):
    # 要設定為 IntegerField or AutoField 才會有 Auto increment 效果
    f = models.AutoField(max_length=100, primary_key=True)
    label = models.TextField()

    # add a custom mdoelManager QuerySet
    # theH.person.authors()
    # theH.person.editors()
    person = person()

    # 必須 override objects 成員
    # theH.objects.all() 等於 get_queryset() 回覆的結果
    objects = myManager()
    
    class Meta: 
        app_label = 'model_folder'
        db_table = 'theH'
