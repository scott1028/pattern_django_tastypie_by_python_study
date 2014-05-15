# coding:utf-8
# 這個檔案要自己建立。
# 這個檔案可以隨便放只要你相關的 Model 可以載入就好。所以不一定要放在 app_folder/api.py 下。
# 本範例為 NestResource 展示
# API為：
# /api6/product_resource/2/package/?format=json
# /api6/product_resource/1/package/?format=json
# /api6/product_resource/?format=json
# /api6/product_resource/1/?format=json
# /api7/package_resource/?format=json
# /api7/package_resource/1/?format=json

from tastypie.resources import ModelResource
from nested.models import package, product
from tastypie.serializers import Serializer

# CUD 將要求輸入使用者帳號密碼
# from tastypie.authentication import BasicAuthentication
# 不需驗證使用者
from tastypie.authentication import Authentication
from tastypie.authentication import SessionAuthentication

from tastypie.authorization import Authorization

from tastypie import fields
from tastypie.serializers import Serializer
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf.urls import patterns, url
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


# 設定這個 API 回復的內容
class package_resource(ModelResource):

    # 必須其中一個設定為 full = False, 將影響是展現 relation resource url 或是 object 資料
    # 千萬不可以兩個都設定為 full = True 會陷入無線迴圈！
    # 除非你需要潮狀資料顯示才需要這樣設定。
    # 如果已經有類似 url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/package%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_package_list'), name="api_get_package_list"), 
    # 方式直接呼叫另一個 resource 的 create_response 可以不用設定這個部分，就能運作了，內部 filter 規則套用 django model 的機制！
    products = fields.ManyToManyField('nested.api.resource.product_resource', 'product_set', full=False)

    class Meta:
        # 搜尋資料的依據
        queryset = package.objects.all()

        # 成為網址的 Resource
        resource_name = 'package_resource'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = [] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = [] # all support is default

        # 因為 relational resource 直接呼叫 packageResource.get_list 取得物件了, 所以 allowed_method 都不被過濾

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            'package_name': 'exact gt gte lt lte',
            # 打開 Django 的 Relational Model QuerySet Filter 規則給 ManyToMany 的 products 屬性。
            'products': ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data['resource_type']='package_resource'
        return bundle

    def dispatch(self, request_type, request, **kwargs):

        # import pdb;pdb.set_trace()

        return super(package_resource,self).dispatch(request_type, request, **kwargs)

    def get_list(self, request, **kwargs):
        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))

        # 使用 Django Model 的 Relational QuerySet 機制再過濾資料一次。
        # 要注意這個是共用方法, 所以要避開當直接存取 package_resource 的時候,
        # 不會有 kwargs['product'] 物件的條件。
        if 'product' in kwargs:
            objects = objects.filter(product=kwargs['product'])

        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(), limit=self._meta.limit, max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

# 設定這個 API 回復的內容
class product_resource(ModelResource):

    # 設定 full = True 可以產生巢狀資料, 設定 full = False 將僅產生巢狀的 URL。
    packages = fields.ManyToManyField(package_resource, 'packages', full=True)
    
    class Meta:
        # 搜尋資料的依據
        queryset = product.objects.all()

        # 成為網址的 Resource
        resource_name = 'product_resource'

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get', 'post'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch'] # all support is default

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            'product_name': 'exact gt gte lt lte',
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/package%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_package_list'), name="api_get_package_list"),
        ]

    def get_package_list(self, request, **kwargs):
        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        packageResource = package_resource()

        # 將 product_id 傳給 package_resource 的 get_list Method, 並使用 Django Model 的 Relational QuerySet 機制來過濾資料。
        # 或著 return packageResource.get_list(request, product__id=obj.id),
        # 其 package_resource 的 QuerySet Filter 亦改為 objects.filter(product__id=kwargs['product__id'])。
        # .get_list 已經是直接跳過 package_resource 的 list_allowed_methods, detail_allowed_methods 檢查機制了。所以另一邊不用設定
        # 檢查可否使用 get post put patch delete 等方法在 .dispatch 內之 .method_check 檢查, 跳過他直接使用 get_list 就好了。
        return packageResource.get_list(request, product=obj)