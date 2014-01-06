# coding:utf-8

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# tastypie
from tastypie.api import Api

# 引入剛剛定義的 tastypie resource api
from book.api.resource import first_book_resource

first_book_api=Api(api_name='first_book_api')
first_book_api.register( first_book_resource() )

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_tastypie_pattern.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(first_book_api.urls)),
    # 根據 Tastypie 的 API 設計風格
    #
    # 觀看 api 有那些東西
    # /api/{api_name}/?format=json
    # 	/api/first_book_api/?format=json
    #
    # 資料讀取
    # /api/{api_name}/{app_name}/?format=json
    # 	/api/first_book_api/first_book/?format=json
    #
    # 資料表 schema
    # /api/{api_name}/{app_name}/schema/?format=json
    #	/api/first_book_api/first_book/schema/?format=json
    #

    # 根據上述 api 的格式，所以 api_name 要命名好！
)
