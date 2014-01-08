# coding:utf-8
# 這個檔案要自己建立。
# 這個檔案可以隨便放只要你相關的 Model 可以載入就好。所以不一定要放在 app_folder/api.py 下。

from tastypie.resources import ModelResource
from book.models import first_book

# 設定這個 API 回復的內容
class first_book_resource(ModelResource):
    class Meta:
        queryset = first_book.objects.all()
        resource_name = 'first_book'

        # 定義可接受的方法
        allowed_methods = ['get','post','put','delete']
        pass