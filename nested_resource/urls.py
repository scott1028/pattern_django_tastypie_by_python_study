# coding:utf-8

from django.conf.urls import patterns, include, url

from nested_resource.resource import *

urlpatterns = patterns(
    '',
    # 因為這邊有一個 /theA_resouce/ 開頭的 URL 設定
    url(r'', include(theB_resource().urls)),

    url(r'', include(theA_resource().urls)),
)