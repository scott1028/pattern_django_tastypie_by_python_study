# coding:utf-8
# 這個檔案要自己建立。
# 這個檔案可以隨便放只要你相關的 Model 可以載入就好。所以不一定要放在 app_folder/api.py 下。

from tastypie.resources import ModelResource
from book.models import first_book
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

# 似乎預設的 Ajax 就是使用 content-type: application/x-www-form-urlencoded
# import urlparse
# class urlencodeSerializer(Serializer):

#     formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']

#     content_types = {
#         'json': 'application/json',
#         'jsonp': 'text/javascript',
#         'xml': 'application/xml',
#         'yaml': 'text/yaml',
#         'html': 'text/html',
#         'plist': 'application/x-plist',
#         'urlencode': 'application/x-www-form-urlencoded',
#     }

#     # 實作轉換部分
#     def from_urlencode(self, data,options=None):
#         """ handles basic formencoded url posts """
#         qs = dict((k, v if len(v)>1 else v[0] )
#             for k, v in urlparse.parse_qs(data).iteritems())
#         return qs

#     def to_urlencode(self,content):
#         pass

from tastypie.serializers import Serializer
import time
import json
from django.core.serializers.json import DjangoJSONEncoder

# class CustomJSONSerializer(Serializer):
#     # 回應給 Client
#     def to_json(self, data, options=None):
#         options = options or {}

#         data = self.to_simple(data, options)

#         # Add in the current time.
#         data['requested_time'] = time.time()

#         return json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)

#     # 從 Client 接收
#     def from_json(self, content):
#         data = json.loads(content)

#         if 'requested_time' in data:
#             # Log the request here...
#             pass

#         return data

# 設定這個 API 回復的內容
class first_book_resource(ModelResource):
    class Meta:
    	# 搜尋資料的依據
        queryset = first_book.objects.all()

        # 成為網址的 Resource
        resource_name = 'first_book'

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get', 'post'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch'] # all support is default

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
    		'title': 'exact gt gte lt lte',
		}

        # 總是回復資料
        # 如果沒設定 put post patch 會沒有 Response, delete 本身維持沒有 Response
        always_return_data = True

        # 可用來替除這個 Model 要顯示在 Response JSON 的 Field
        # excludes = ['title']

		# 如果要製作 CRUD Restful API 必須在額外設定以下：資料序列化、用戶驗證、用戶權限(預設只有 ReadOnly)
		# 參考：http://django-tastypie.readthedocs.org/en/latest/resources.html#resource-options-aka-meta

        # 資料序列化, 如果要使用 Ajax Post 這邊要寫成這樣(至少要實作 Serializer 才會有回應, 與接收資料)
        # 參考：http://django-tastypie.readthedocs.org/en/latest/serialization.html#implementing-your-own-serializer
        # serializer = urlencodeSerializer() # 客製化
        # serializer = CustomJSONSerializer() # 客製化
        serializer = Serializer() # 預設

        # 驗證用戶是誰(Authentication, BasicAuthentication, ApiKeyAuthentication, SessionAuthentication, DigestAuthentication, OAuthAuthentication, MultiAuthentication)
        
        # 無視存取權限(簡單來說就是開放式存取, 不需要認證)
        authentication = Authentication()

        # 必須先使用 http://127.0.0.1:3333/admin 登入後拿到的 csrf token 就可以用這個 session auth 存取了
        # authentication = SessionAuthentication()

        # 用戶的權限(Authorization, ReadOnlyAuthorization, DjangoAuthorization)
        authorization = Authorization()

    #
    # 從 Django Model to Json 的過程會調用。可以用來增加欄位
    def dehydrate(self, bundle):
        bundle.data['custom_field'] = "Whatever you want"
        return bundle

    #
    # 負責 Response: /api/first_book/?format=json
    def get_list(self, request, **kwargs):
        # print 'recv request list'

        # print dir(request)

        # 似乎會寫目前是由誰訪問(通常是 AnonymousUser 字串)
        # print request.user

        # 測試一下 bundle 的資料處理功能(可以改變原先的吞吐資料)
        # 參考：http://django-tastypie.readthedocs.org/en/latest/bundles.html
        # 參考：http://django-tastypie.readthedocs.org/en/latest/resources.html#build-bundle
        # bundle = self.build_bundle(obj=req_uest.user, data={'a':1}, request=request)
        # bundle = self.alter_detail_data_toserialize(request, bundle)

        # json_data=super(first_book_resource,self).get_list(request, **kwargs)

        # print json_data

        # import pdb;pdb.set_trace();

        # return json_data

        # return '0'
        # return self.create_response(request, None)

        base_bundle = self.build_bundle(request=request)
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

        # 包含 meta header
        # return self.create_response(request, to_be_serialized)
        # 去除 meta header, only data list
        return self.create_response(request, bundles)

    # 可用來修改上傳的資料
    def hydrate(self, bundle):
        # import pdb;pdb.set_trace();
        # bundle.data[u'title']=u'scott modify data in hydrate method!'

        # defined field test
        bundle.data[u'body']=u'scott put test body content in hydrate method override!'

        # not extist field test, it will not raise error.
        bundle.data[u'test_field']=u'test field'

        return bundle