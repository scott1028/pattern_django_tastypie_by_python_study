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


**Resource Relational Sample**

    ::

        # 資料表關聯(似乎是互相 ManyToMany 關聯)
            Group has many users,permissions [使用 users, permissions 命名]
            Users has many groups, too [使用 groups 命名]
            Permission has many Group, too [使用 group_set 命名]

            *User don't have any permission relation setting, it uses is_supperuser column flag.

        # api/resource.py
        class GroupModelResource(ModelResource):

            # 其實 user_set 類型等於底下的 groups, 都是 <django.db.models.fields.related.ManyRelatedManager object>
            # 應該只是內部定義名稱的屬性明稱不同而已。
            users = fields.ToManyField('api.resource.UserModelResource','user_set')

            class Meta:
                queryset = Group.objects.all()
                resource_name = 'group'
                allow_methods = ['get']

        class PermissionModelResource(ModelResource):
            class Meta:
                queryset = Permission.objects.all()
                resource_name = 'permission'
                allow_methods = ['get']

        class UserModelResource(ModelResource):

            groups = fields.ToManyField('api.resource.GroupModelResource','groups')
            permissions = fields.ToManyField('api.resource.PermissionModelResource','user_permissions')

            class Meta:
                queryset = User.objects.all()
                resource_name = 'user'
                allow_method = ['get']
            pass


**搭配 Vagrant 啟動專案**

    ::

        # Vagrantfile
          config.vm.network :forwarded_port, guest: 80, host: 8080
          代表 sudo python manage.py runserver 0.0.0.0:80 將被導入 host 的 127.0.0.1:8080
          0.0.0.0 IP 位置必須填寫, 若直接填寫 80 將無法正確連線!


**Restful CRUD Resource & Ajax**

    ::

        # Resource 接收到 Request/Response 運作流程
          參考：http://django-tastypie.readthedocs.org/en/latest/resources.html#flow-through-the-request-response-cycle

        # 驗證用戶為誰
          參考：http://django-tastypie.readthedocs.org/en/latest/authentication.html

        # 使用者權限
          參考：http://django-tastypie.readthedocs.org/en/latest/authorization.html
          
        # 資料吞吐 Serializer
          參考：http://django-tastypie.readthedocs.org/en/latest/serialization.html#implementing-your-own-serializer

        # book/api/resource.py
                ...
            # 設定這個 API 回復的內容
            class first_book_resource(ModelResource):
                class Meta:
                    # 搜尋資料的依據
                    queryset = first_book.objects.all()

                    # 成為網址的 Resource
                    resource_name = 'first_book'

                    # 照抄 detail_allowed_methods=list_allowed_methods, 允許接受 Client Request 訪問的方法,
                      預設有 get 如果設定為 [] 將無法使用這個 Resource。
                    list_allowed_methods = ['get', 'post', 'put', 'delete', 'patch'] # all support is default

                    # (*)定義 Restful 支援的方法有哪些, 如果沒寫進去就伺服器就不支援(只需要設定這個即可)
                    detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch'] # all support is default

                    # 定義可以接受 Client Request Query String 的欄位與規則
                      ex: /api/first_book/?format=json&title=test
                    filtering = {
                        'title': 'exact gt gte lt lte',
                    }

                    # 可用來替除這個 Model 要顯示在 Response JSON 的 Field
                    # excludes = ['title']

                    # 如果要製作 CRUD Restful API 必須在額外設定以下：資料序列化、用戶驗證、用戶權限(預設只有 ReadOnly)
                    # 參考：http://django-tastypie.readthedocs.org/en/latest/resources.html#resource-options-aka-meta

                    # 資料序列化, 如果要使用 Ajax Post 這邊要寫成這樣(至少要實作 Serializer 才會有回應, 與接收資料)
                    serializer = Serializer() # 預設

                    # 驗證用戶是誰
                    authentication = Authentication()

                    # 用戶的權限
                    authorization = Authorization()
                ...

        # static/index.html
                ...
            // post
            var test_post_first_book_api=function(){
                $.ajax({
                    url:'/api/first_book/?format=json',
                    data:'{"title":"create by post with content-type/json'+(new Date).toJSON()+'"}',
                    type:'post',
                    contentType:'application/json',
                    success:function(res,status,xhr){
                        console.log(res);
                    }
                    // 補充說明：
                    // contentType:'application/x-www-form-urlencoded; charset=UTF-8',
                       預設這個 Tastypie 並不支援要自己實做。
                    // processData: false, // 預設為開啟，將對 data 的 JavaScript 物件做 urlencode, 
                    // 如果使用 application/json 就不用開啟, 但是 data 參數要記得用 JSON.stringify 轉換成 JSON
                });
            };

            // put, 可用於更新資料(這個算是替換資料, 會整筆被換掉類似 Ext.apply)
            var test_put_first_book_api_by_id=function(id){
                $.ajax({
                    url:'/api/first_book/'+id.toString()+'/?format=json',
                    // 如果要更新部分資料原本的欄位依然要補齊
                    data:'{"title":"create by put with content-type/json'+(new Date).toJSON()+'"}',
                    type:'put',
                    contentType:'application/json',
                    success:function(res,status,xhr){
                        console.log(res);
                    }
                });
            };
                ...