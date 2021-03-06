# coding:utf-8

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# 引入剛剛定義的 tastypie resource api
from book.api.resource import first_book_resource

# 引入剛剛定義的 tastypie resource api
from article.api.resource import article_resource
from article.api.resource import reporter_resource

from api.resource import UserModelResource,PermissionModelResource,GroupModelResource

# 引入 people
from people.api.resource import people_resource

from multi_resource.api.resource import multi_resource

from nested.api.resource import *

from nested_resource_2.resource import *

from crud_resource.resource import *

from book.api.multipart_test import *

from public.api import *

# print article_resource().urls
# print reporter_resource().urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_tastypie_pattern.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^tastypie/', include(upload().urls)),
    url(r'^tastypie/', include(upload_query().urls)),
    # url(r'', include(api.DuoSIMBatchModelResource().urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(first_book_resource().urls)),
    url(r'^api2/', include(article_resource().urls)),
    url(r'^api3/', include(reporter_resource().urls)), # 代表不允許直接存取 reporter_resource api, 從 urls.py 內關閉

    url(r'^api4/', include(UserModelResource().urls)),
    url(r'^api4/', include(GroupModelResource().urls)),
    url(r'^api4/', include(PermissionModelResource().urls)),

    # test session auth access
    url(r'^book/test', 'book.views.test'),
    url(r'^book/upload', 'book.views.upload'),
    url(r'^book/upload_query', 'book.views.upload_query'),

    # SessionAuthorization
    url(r'^api5/', include(people_resource().urls)),
    url(r'^api5/c_login', 'people.views.c_login'), # implement user login enterance
    url(r'^api5/index', 'people.views.index'), # test SessionAuthentication For CRUD

    # Nested Resource 設定
    url(r'^api6/', include(product_resource().urls)),
    # url(r'^api7/', include(package_resource().urls)),
    # 可以不用設定 package_resource, 靠 product_resource 使用 nested package_resource 就可以達成了！
    
    # 分離 url pattern 設定, 因為沒有放在 api 目錄下所以預設 url 將自動去除 /api/ pre-router
    url(r'', include('nested_resource.urls')),

    # url(r'^api7/', include(multi_resource().urls)),

    url(r'', include(theA_resource2().urls)),
    url(r'', include(theB_resource2().urls)),
    url(r'', include(theC_resource2().urls)),
    url(r'', include(theD_resource2().urls)),
    url(r'', include(theE_resource2().urls)),
    url(r'', include(theA_resource3().urls)),
    url(r'', include(theB_resource3().urls)),
    
    url(r'', include(public().urls)),
    # 根據 Tastypie 的 API 設計風格
    #
    # 觀看 api 有那些東西
    # /api/{resource_name}/?format=json
    # 	/api/first_book/?format=json
    #
    # 資料讀取
    # /api/{resource_name}/?format=json
    # 	/api/first_book/?format=json
    #
    # 資料表 schema
    # /api/{resource_name}/schema/?format=json
    #	/api/first_book/schema/?format=json
    #

    # POST, PUT
    # 以上都是透過 GET 方法取得資料，
    # 當我們進行 POST / PUT 時會發生錯誤，這是因為沒有對他進行權限的設定。
    # 參考：http://techblog.insureme.com.tw/2012/03/tastypie-django-api.html
    #

    # 根據上述 api 的格式，所以 api_name 要命名好！
)
