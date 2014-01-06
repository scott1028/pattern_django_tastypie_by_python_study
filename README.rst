====================
Django-Tastypie 範例
====================

**參考文獻**

    ::

        # Base API
            http://django-tastypie.readthedocs.org/en/latest/index.html#quick-start
            
        # REST API
            http://django-tastypie.readthedocs.org/en/latest/resources.html


**架構流程**

    ::

        1. django-admin startproject myProject
        2. manage.py startapp myApp
        3. 修改 /myApp/models.py 增加一個 model class 例如：first_book(models.Model)
        4. 修改 /myProject/settings.py 內的 INSTALLED_APPS
           增加：
                'tastypie','book'

        5. 增加 API 文件，例如/book/api/resource.py，定義 API 的 Model 設定：
            from tastypie.resources import ModelResource
            from book.models import first_book

            # 設定這個 API 回復的內容
            class first_book_resource(ModelResource):
                class Meta:
                    queryset = first_book.objects.all()
                    resource_name = 'first_book'
                    allowed_methods = ['get']
                    pass

        6. 修改 /myProject/urls.py：
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
                #   /api/first_book_api/?format=json
                #
                # 資料讀取
                # /api/{api_name}/{app_name}/?format=json
                #   /api/first_book_api/first_book/?format=json
                #
                # 資料表 schema
                # /api/{api_name}/{app_name}/schema/?format=json
                #   /api/first_book_api/first_book/schema/?format=json
                #

                # 根據上述 api 的格式，所以 api_name 要命名好！
            )

