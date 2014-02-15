# coding:utf-8

# 重點精華
#   在本範例我們得知不管是 get list, details, 都會統一呼叫 get_object_list 方法, 差別在單一的時候只取 [0], 並且內部都是使用 meta.queryset 那個 Django Model 來運作
#   get list 的時候會額外將 request 的 query string 套入 filter 再丟給 queryset 過濾一次資料。
#   get details 就直接使用 kwargs 來過濾 query string 將完全不會轉入。(這點要注意)

from tastypie.resources import ModelResource
from nested_resource_2.models import *
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

from django.conf import settings
from django.conf.urls import patterns, url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.core.urlresolvers import NoReverseMatch, reverse, resolve, Resolver404, get_script_prefix
from django.core.signals import got_request_exception
from django.db import transaction
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql.constants import QUERY_TERMS
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.utils.cache import patch_cache_control, patch_vary_headers
from django.utils import six

from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.bundle import Bundle
from tastypie.cache import NoCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse, Unauthorized
from tastypie import fields
from tastypie import http
from tastypie.paginator import Paginator
from tastypie.serializers import Serializer
from tastypie.throttle import BaseThrottle
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from tastypie.utils.mime import determine_format, build_content_type
from tastypie.validation import Validation

# If ``csrf_exempt`` isn't present, stub it.
try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    def csrf_exempt(func):
        return func


# 設定這個 API 回復的內容
class theA_resource2(ModelResource):

    # 必須其中一個設定為 full = False, 將影響是展現 relation resource url 或是 object 資料
    # 千萬不可以兩個都設定為 full = True 會陷入無線迴圈！
    # 除非你需要潮狀資料顯示才需要這樣設定。
    # 如果已經有類似 url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/package%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_package_list'), name="api_get_package_list"), 
    # 方式直接呼叫另一個 resource 的 create_response 可以不用設定這個部分，就能運作了，內部 filter 規則套用 django model 的機制！
    # products = fields.ManyToManyField('nested.api.resource.product_resource', 'product_set', full=False)

    class Meta:
        # 搜尋資料的依據
        queryset = theA.objects.all()

        # 成為網址的 Resource
        resource_name = 'theA_resource2'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 因為 relational resource 直接呼叫 packageResource.get_list 取得物件了, 所以 allowed_method 都不被過濾

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        # 對應 relational resource 的 filtering 設定允許
        filtering = {
            'a': ALL,
        }



# 設定這個 API 回復的內容
class theB_resource2(ModelResource):
    # 對應 filtering 的設定
    # 不會影響 (?P<resource_name>%s)/(?P<%s>.*?)/theA_resource2/(?P<a__a>.*?) 的過濾計算
    # 第二個參數是 nested_resource_2.resource.theA_resource2 QuerySet 物件的屬性
    a_set = fields.ToOneField('nested_resource_2.resource.theA_resource2', 'a', full=True)

    class Meta:
        # 搜尋資料的依據
        queryset = theB.objects.all()

        # 成為網址的 Resource
        resource_name = 'theB_resource2'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 因為 relational resource 直接呼叫 packageResource.get_list 取得物件了, 所以 allowed_method 都不被過濾

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            # 打開 Django 的 Relational Model QuerySet Filter 規則給 ManyToMany 的 products 屬性。
            # ToOneField 之 details 的時候似乎不會過濾資料, 似乎 detail toOneRecord 不會運作
            # 注意：get resourceB details 的時候無法使用 relational resource 來 filtering
            'a_set': ALL_WITH_RELATIONS, # 透過 a_set 來濾出 b list 資料
            'b': ALL # 可以讓他在 get_list 的時候透過 b(id) = ? 來 Query, 但是在 B List 的時候 Kwargs 傳不進去
        }

    def dispatch_detail(self, request, **kwargs):

        return super(theB_resource2,self).dispatch_detail(request, **kwargs)

    def get_detail(self, request, **kwargs):
        

        return super(theB_resource2,self).get_detail(request, **kwargs)

    def base_urls(self):
        """
        The standard URLs this ``Resource`` should respond to.
        """
        return [
            # 根據 Django Model Filtering 的錯誤訊息, 參數名稱必須改為 a__a, 才可以順利轉換成 a 剛好是 theA Model 的 primary key
            # 這算一種 hack 寫法, 不需要額外設定 resource 選項
            url(r"^(?P<resource_name>%s)/(?P<%s>.*?)/theA_resource2/(?P<a__a>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
                                                                     # <a> 也可以或是加上前奏詞 ?__field 亦可, ?__ 會被自動去除
                                                                     # 前奏詞彙將是 theB Model 內 Relation Field 或純 Field 詞彙
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            #url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_schema'), name="api_get_schema"),
            #url(r"^(?P<resource_name>%s)/set/(?P<%s_list>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<%s>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]


# 設定這個 API 回復的內容
class theC_resource2(ModelResource):
    # 對應 filtering 的設定
    # 不會影響 (?P<resource_name>%s)/(?P<%s>.*?)/theA_resource2/(?P<a__a>.*?) 的過濾計算
    # 第二個參數是 nested_resource_2.resource.theA_resource2 QuerySet 物件的屬性
    ds = fields.ToManyField('nested_resource_2.resource.theD_resource2', 'thed_set', full=False)

    # 其實如果要制定完整的 api 其實 Model 雙方都用 manayToMany 最為恰當, 因為兩邊都會是 QuerySet 就可以再透過 filter 過濾資料

    class Meta:
        # 搜尋資料的依據
        queryset = theC.objects.all()

        # 成為網址的 Resource
        resource_name = 'theC_resource2'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 因為 relational resource 直接呼叫 packageResource.get_list 取得物件了, 所以 allowed_method 都不被過濾

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            # 打開 Django 的 Relational Model QuerySet Filter 規則給 ManyToMany 的 products 屬性。
            # ToOneField 之 details 的時候似乎不會過濾資料, 似乎 detail toOneRecord 不會運作
            # 注意：get resourceB details 的時候無法使用 relational resource 來 filtering
            # 'ds': ALL_WITH_RELATIONS,
            # 'b': ALL # 可以讓他在 get_list 的時候透過 b(id) = ? 來 Query, 但是在 B List 的時候 Kwargs 傳不進去
        }

# 設定這個 API 回復的內容
class theD_resource2(ModelResource):
    # 對應 filtering 的設定
    # 不會影響 (?P<resource_name>%s)/(?P<%s>.*?)/theA_resource2/(?P<a__a>.*?) 的過濾計算
    # 第二個參數是 nested_resource_2.resource.theA_resource2 QuerySet 物件的屬性
    cs = fields.ToManyField('nested_resource_2.resource.theC_resource2', 'c', full=True)

    class Meta:
        # 搜尋資料的依據
        queryset = theD.objects.all()

        # 成為網址的 Resource
        resource_name = 'theD_resource2'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 因為 relational resource 直接呼叫 packageResource.get_list 取得物件了, 所以 allowed_method 都不被過濾

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            # 打開 Django 的 Relational Model QuerySet Filter 規則給 ManyToMany 的 products 屬性。
            # ToOneField 之 details 的時候似乎不會過濾資料, 似乎 detail toOneRecord 不會運作
            # 注意：get resourceB details 的時候無法使用 relational resource 來 filtering
            'd': ALL,
            # 'cs': ALL_WITH_RELATIONS, # 透過 a_set 來濾出 b list 資料
            # 'b': ALL # 可以讓他在 get_list 的時候透過 b(id) = ? 來 Query, 但是在 B List 的時候 Kwargs 傳不進去
        }
        # trace Tastypie Code 發現 get_details 將不會調用任何有關 build_filter 與 apply_filter 的動作

    # step 0
    def dispatch(self, request_type, request, **kwargs):

        print 1
        # import pdb; pdb.set_trace()

        return super(theD_resource2, self).dispatch(request_type, request, **kwargs)

    # step 1
    def get_list(self, request, **kwargs):

        print 2

        """
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        # TODO: Uncached for now. Invalidation that works for everyone may be
        #       impossible.
        base_bundle = self.build_bundle(request=request)

        # step 2 部分(將驗證 filter, auth 等權限)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        
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

    # step 2, 會將 client URI 的 Query String update 到 filters 內
    # step 2, 將在 return 變數給 step 1 的某一個變數
    def obj_get_list(self, bundle, **kwargs):

        print 3

        """
        A ORM-specific implementation of ``obj_get_list``.

        Takes an optional ``request`` object, whose ``GET`` dictionary can be
        used to narrow the query.
        """
        filters = {}

        if hasattr(bundle.request, 'GET'):
            # Grab a mutable copy.
            filters = bundle.request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)

        # import pdb;pdb.set_trace()

        # 建立 filter 有哪些, 透過 fiterings = { ... } 來把可以 filter 的關鍵字建立出來。
        applicable_filters = self.build_filters(filters=filters)

        try:
            # 透過這些 filters 將物件取出
            objects = self.apply_filters(bundle.request, applicable_filters)

            # 檢查是否有權限可以讀取這個 resource
            return self.authorized_read_list(objects, bundle)
        except ValueError:
            raise BadRequest("Invalid resource lookup data provided (mismatched type).")


    def build_filters(self, filters=None):

        print 4

        # 把 Query String 轉入 filters 內

        import pdb;pdb.set_trace()

        return super(theD_resource2, self).build_filters(filters)

    # 
    # get 單一資料的運作流程, 並沒有將 Query String 轉入 kwargs 所以後面不管加啥參數都沒有用
    # 這部分要自己實做。get_details 為最後一步驟, 必須產生 response
    # 
    def get_detail(self, request, **kwargs):

        print 2

        """
        Returns a single serialized resource.

        Calls ``cached_obj_get/obj_get`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        basic_bundle = self.build_bundle(request=request)

        try:
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)

    #
    # 所有單一資料都會呼叫複數資料再使用 filter 過濾出單一資料
    #
    def cached_obj_get(self, bundle, **kwargs):

        print 3

        # import pdb;pdb.set_trace()

        """
        A version of ``obj_get`` that uses the cache as a means to get
        commonly-accessed data faster.
        """
        cache_key = self.generate_cache_key('detail', **kwargs)
        cached_bundle = self._meta.cache.get(cache_key)

        if cached_bundle is None:
            # 在這裡看出他只用 kwargs 就過濾資料了, 沒有使用 request.GET 內的 Query String 的的條件
            # 可是如果設計在 kwargs 他是使用 meta.queryset.filter(kwargs) 基本上是套用 Django 的 Model Filter 關鍵字規則。
            cached_bundle = self.obj_get(bundle=bundle, **kwargs)
            self._meta.cache.set(cache_key, cached_bundle)

        return cached_bundle

    def get_object_list(self, request):

        print 'list, detail 都會呼叫這個！ (get_object_list) '

        """
        An ORM-specific implementation of ``get_object_list``.

        Returns a queryset that may have been limited by other overrides.
        """
        return self._meta.queryset._clone()
