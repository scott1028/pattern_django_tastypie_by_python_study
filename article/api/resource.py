# coding:utf-8
# 這個檔案要自己建立。
# 這個檔案可以隨便放只要你相關的 Model 可以載入就好。所以不一定要放在 app_folder/api.py 下。

from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

# CUD 將要求輸入使用者帳號密碼
# from tastypie.authentication import BasicAuthentication
# 不需驗證使用者
from tastypie.authentication import Authentication

# 根據 Django-Admin 後台所題設定的使用者權限來驗證
# from tastypie.authorization import DjangoAuthorization
# 不需驗證使用者權限
from tastypie.authorization import Authorization

import time
import json
from django.core.serializers.json import DjangoJSONEncoder

# import my model
from article.models import Reporter
from article.models import Article

from tastypie import fields

# # 增加一個關聯的 Resource, belongs to article_resource
class reporter_resource(ModelResource):

    # reporter hasMany article 條件下。請參考 article.models 內的設定。
    articles = fields.ToManyField('article.api.resource.reporter_resource','article_set')
    # article_set 是 Article Object 的成員，被關聯的 Model 被設定 foreign_key 即可。
    # Reporter.objects.first().article_set.create(headline='create by Reporter Instance',pub_date=datetime.now()) 建立關聯紀錄

    class Meta:
        queryset = Reporter.objects.all()

        resource_name = 'reporter'

        # 照抄 detail_allowed_methods=list_allowed_methods, 允許接受 Client Request 訪問的方法, 預設有 get 如果設定為 [] 將無法使用這個 Resource。
        list_allowed_methods = ['get', 'post'] # all support is default

        # (*)定義 Restful 支援的方法有哪些, 如果沒寫進去就伺服器就不支援(只需要設定這個即可)
        detail_allowed_methods = ['put', 'delete', 'patch'] # all support is default

        # 總是回復資料
        # 如果沒設定 put post patch 會沒有 Response, delete 本身維持沒有 Response
        always_return_data = True

        serializer = Serializer() # 預設

        # 驗證用戶是誰(Authentication, BasicAuthentication, ApiKeyAuthentication, SessionAuthentication, DigestAuthentication, OAuthAuthentication, MultiAuthentication)
        authentication = Authentication()

        # 用戶的權限(Authorization, ReadOnlyAuthorization, DjangoAuthorization)
        authorization = Authorization()

# 設定這個 API 回復的內容
class article_resource(ModelResource):

    # belongs to reporter (like has one)
    # 看來似乎不大對！需要再修改
    reporter_is_who = fields.ToOneField('article.api.resource.article_resource','reporter')

    class Meta:
        # 搜尋資料的依據
        queryset = Article.objects.all()

        # 成為網址的 Resource, 如果沒設定定就會採用 ModelResource 的 Class Name
        resource_name = 'article'

        # 照抄 detail_allowed_methods=list_allowed_methods, 允許接受 Client Request 訪問的方法, 預設有 get 如果設定為 [] 將無法使用這個 Resource。
        list_allowed_methods = ['get', 'post'] # all support is default

        # (*)定義 Restful 支援的方法有哪些, 如果沒寫進去就伺服器就不支援(只需要設定這個即可)
        detail_allowed_methods = ['get','put', 'delete', 'patch'] # all support is default, 讓 rest 只支援 put delete patch 這三個而已, 排除 get 跟 post

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            'headline': 'exact gt gte lt lte',
        }

        # 總是回復資料
        # 如果沒設定 put post patch 會沒有 Response, delete 本身維持沒有 Response
        always_return_data = True

        serializer = Serializer() # 預設

        # 驗證用戶是誰(Authentication, BasicAuthentication, ApiKeyAuthentication, SessionAuthentication, DigestAuthentication, OAuthAuthentication, MultiAuthentication)
        authentication = Authentication()

        # 用戶的權限(Authorization, ReadOnlyAuthorization, DjangoAuthorization)
        authorization = Authorization()

    #
    # 從 Django Model to Json 的過程會調用。可以用來增加欄位
    def dehydrate(self, bundle):
        bundle.data['custom_field'] = "Whatever you want"
        return bundle

    # override get list method
    def get_list(self, request, **kwargs):
        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(
            bundle=base_bundle,
            **self.remove_api_resource_names(kwargs)
        )
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(
            request.GET, sorted_objects,
            resource_uri=self.get_resource_uri(),
            limit=self._meta.limit,
            max_limit=self._meta.max_limit,
            collection_name=self._meta.collection_name
        )
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            # check the user's privilege
            # if request.user.is_superuser or \
            #         obj in Article.objects.filter(
            #             role=request.user.role_set.all()
            #         ):
            if True:
                bundle = self.build_bundle(obj=obj, request=request)
                bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(
            request,
            to_be_serialized
        )

        # print to_be_serialized

        # print self._meta.collection_name

        # print bundles

        # return self.create_response(request, to_be_serialized)
        return self.create_response(request, bundles)

