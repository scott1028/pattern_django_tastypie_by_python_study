# coding:utf-8

# 重點精華
#   在本範例我們得知不管是 get list, details, 都會統一呼叫 get_object_list 方法, 差別在單一的時候只取 [0], 並且內部都是使用 meta.queryset 那個 Django Model 來運作
#   get list 的時候會額外將 request 的 query string 套入 filter 再丟給 queryset 過濾一次資料。
#   get details 就直接使用 kwargs 來過濾 query string 將完全不會轉入。(這點要注意)

from tastypie.resources import ModelResource
from crud_resource.models import *
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

# 不需驗證使用者權限
from tastypie.authorization import Authorization

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

# 設定這個 API 回復的內容
class theA_resource3(ModelResource):

    theb_set=fields.ToManyField('crud_resource.resource.theB_resource3', 'theb_set', full=True)

    class Meta:
        # 搜尋資料的依據
        queryset = theA.objects.all()

        # 成為網址的 Resource
        resource_name = 'theA_resource3'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        filtering = {
            'a': ALL,
        }

        serializer = Serializer()
        authentication = Authentication()
        authorization = Authorization()


# 設定這個 API 回復的內容
class theB_resource3(ModelResource):
    a_set = fields.ToOneField('crud_resource.resource.theA_resource3', 'a', full=False)

    class Meta:
        # 搜尋資料的依據
        queryset = theB.objects.all()

        # 成為網址的 Resource
        resource_name = 'theB_resource3'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get','post','put','patch','delete'] # all support is default

        # 因為 relational resource 直接呼叫 packageResource.get_list 取得物件了, 所以 allowed_method 都不被過濾

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
            'a_set': ALL_WITH_RELATIONS,
            'b': ALL
        }

        serializer = Serializer()
        authentication = Authentication()
        authorization = Authorization()

# 可用的方法有：
# http://127.0.0.1:3333/theA_resource3/?format=json
# 	get, post

# http://127.0.0.1:3333/theA_resource3/{pk}/?format=json
#	put, patch, delete

# 要注意 content-type 必須是 application/json
# 	$.ajax({
# 		url:'/theA_resource3/?format=json',
# 		data:'{
#		    "a": 50,
#		    "label": "eeeee",
#		    "resource_uri": "/theA_resource3/2/",
#		    "theb_set": ["/theB_resource3/1/"]				// 基本上就用 Resource 吐過來的資料吐回去就可以了
#		}',
# 		type:'post',
# 		contentType:'application/json',
# 		success:function(res,status,xhr){
# 			console.log(res);
# 		}
# 		// 補充說明：
# 		// contentType:'application/x-www-form-urlencoded; charset=UTF-8', 預設這個 Tastypie 並不支援要自己實做。
# 		// processData: false, // 預設為開啟，將對 data 的 JavaScript 物件做 urlencode, 
# 		// 如果使用 application/json 就不用開啟, 但是 data 參數要記得用 JSON.stringify 轉換成 JSON
# 	});	