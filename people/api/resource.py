# coding:utf-8
# 這個檔案要自己建立。
# 這個檔案可以隨便放只要你相關的 Model 可以載入就好。所以不一定要放在 app_folder/api.py 下。

from tastypie.resources import ModelResource
from people.models import people
from tastypie.serializers import Serializer

# CUD 將要求輸入使用者帳號密碼
# from tastypie.authentication import BasicAuthentication
# 不需驗證使用者
from tastypie.authentication import Authentication
from tastypie.authentication import SessionAuthentication


# 根據 Django-Admin 後台所題設定的使用者權限來驗證
# from tastypie.authorization import DjangoAuthorization
# 不需驗證使用者權限
from tastypie.authorization import Authorization


from tastypie.serializers import Serializer
import time
import json
from django.core.serializers.json import DjangoJSONEncoder


# 設定這個 API 回復的內容
class people_resource(ModelResource):
    class Meta:
        # 搜尋資料的依據
        queryset = people.objects.all()

        # 成為網址的 Resource
        resource_name = 'people'

        # 照抄 detail_allowed_methods=list_allowed_methods, 允許接受 Client Request 訪問的方法, 預設有 get 如果設定為 [] 將無法使用這個 Resource。
        list_allowed_methods = ['get', 'post'] # all support is default

        # (*)定義 Restful 支援的方法有哪些, 如果沒寫進去就伺服器就不支援(只需要設定這個即可)
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch'] # all support is default

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            'name': 'exact gt gte lt lte',
        }

        # 總是回復資料
        # 如果沒設定 put post patch 會沒有 Response, delete 本身維持沒有 Response
        always_return_data = True

        serializer = Serializer() # 預設

        # 驗證用戶是誰(Authentication, BasicAuthentication, ApiKeyAuthentication, SessionAuthentication, DigestAuthentication, OAuthAuthentication, MultiAuthentication)
        
        # 無視存取權限(簡單來說就是開放式存取, 不需要認證)
        authentication = SessionAuthentication()

        # 必須先使用 http://127.0.0.1:3333/admin 登入後拿到的 csrf token 就可以用這個 session auth 存取了
        # authentication = SessionAuthentication()

        # 用戶的權限(Authorization, ReadOnlyAuthorization, DjangoAuthorization)
        authorization = Authorization()