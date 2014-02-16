# coding:utf-8
# 達成：http://127.0.0.1:3333/theA_resource/2/theB_resource/1/?format=json
# double resource 的特殊寫法，可以與 nested app 寫法與 cookbook 上的比較！

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

# 不需驗證使用者
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from django.conf.urls import patterns, url

from nested_resource.models import *


# 設定這個 API 回復的內容
class theA_resource(ModelResource):

    # 參考 model 來設定即可
    thebs = fields.ToManyField('nested_resource.resource.theB_resource', 'theb_set', full=False)

    class Meta:
        # 搜尋資料的依據
        queryset = theA.objects.all()

        # 成為網址的 Resource
        resource_name = 'theA_resource'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get', 'post', 'put', 'delete','patch'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get', 'post', 'put', 'delete','patch'] # all support is default

        authentication = Authentication()
        authorization = Authorization()

        # 匹配 theB filtering
        filtering = {
            # 由於 theB_resouce 有設定 filtering = { thea: ALL_WITH_RELATIONS }, 所以 theA_resouce 必須要開啟 a 的 filtering 否則會跳錯
            'a': ALL
        }


# 設定這個 API 回復的內容
class theB_resource(ModelResource):

    # 參考 model 來設定即可(model 為 foregin_key, 所以是 manyToOne)
    thea = fields.ToOneField('nested_resource.resource.theA_resource', 'a', full=True)

    class Meta:
        # 搜尋資料的依據
        queryset = theB.objects.all()

        # 成為網址的 Resource
        resource_name = 'theB_resource'

        # Default is None, which means delegate to the more specific like list_allowed_methods, detail_allowed_methods
        allowed_methods = None

        # 定義 multi record 的存取權限有哪些
        list_allowed_methods = ['get', 'post', 'put', 'delete','patch'] # all support is default

        # 定義 single record 的存取權限有哪些
        detail_allowed_methods = ['get', 'post', 'put', 'delete','patch'] # all support is default

        authentication = Authentication()
        authorization = Authorization()

        # 匹配 theA filtering
        filtering = {
            # 打開 Django 的 Relational Model QuerySet Filter 規則給 ToOne 的 theA 屬性。
            'thea': ALL_WITH_RELATIONS
        }

    def prepend_urls(self):
        return [
            # url(r"^theA_resource/(?P<theA_resource_id>\w[\w/-]*)/(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            
            # 利用上述的 relational filtering 把 theA_resource_id 改為 thea__a 就可以了達成目的了！
            url(r"^theA_resource/(?P<thea__a>\w[\w/-]*)/(?P<resource_name>%s)/(?P<%s>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^theA_resource/(?P<thea__a>\w[\w/-]*)/(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
        ]

    def dispatch_detail(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) on
        a single resource.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """

        # list 似乎不會跳錯, 但是 details 似乎會有錯誤。
        # hacking 當達到條件是 /theA_resource/2/theB_resource/4/?format=json 時,
        # 會產生 Cannot resolve keyword u'thea' into field. Choices are: a, b, label 問題很怪。
        # 目前採用此方法解決！
        if set(kwargs.keys())=={u'pk',u'resource_name',u'thea__a'}:
            kwargs['a_id']=kwargs['thea__a']
            del(kwargs['thea__a'])

        return self.dispatch('detail', request, **kwargs)
