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
          代表 sudo python manage.py runserver 0.0.0.0:80 將被導入 Host 的 127.0.0.1:8080
          0.0.0.0 IP 位置必須填寫, 若直接填寫 80 將無法正確連線!

          ifconfig
          查詢會有 virtualbox 的 10.0.2.15 與 127.0.0.1 的 ip
          若 config.vm.network :forwarded_port, guest: 3333, host: 3333
          python manage.py runserver 10.0.2.15:3333 將會導向 Host 的 127.0.0.1:3333
            或
          python manage.py runserver 0.0.0.0:3333 將會導向 Host 的 127.0.0.1:3333



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

        # Restful Ajax 進階應用(巢狀存取), 要注意 content-type 必須是 application/json
                ...
            $.ajax({
                url:'/theA_resource3/?format=json',
                data:'{
                  "label": "application/json add b",
                  "theb_set": [{
                    "b": 4,                             // 有打 b: 4 就會是 patch
                    "a_set": "/theA_resource3/4/",
                    "label": "999950"
                  },
                  {
                    "a_set": "/theA_resource3/4/",     // 沒有指定 b 將變為 create
                    "label": "92222950"
                  },
                  {
                    "a_set": "/theA_resource3/4/",
                    "label": "950"
                    },
                  {
                    "a_set": "/theA_resource3/4/",
                    "label": "99"
                  }]
                }',
                type:'post',
                contentType:'application/json',
                success:function(res,status,xhr){
                    console.log(res);
                }
                // 補充說明：
                // contentType:'application/x-www-form-urlencoded; charset=UTF-8', 預設這個 Tastypie 並不支援要自己實做。
                // processData: false, // 預設為開啟，將對 data 的 JavaScript 物件做 urlencode, 
                // 如果使用 application/json 就不用開啟, 但是 data 參數要記得用 JSON.stringify 轉換成 JSON
            }); 
                ...


**Add south package support**

    ::


        # install south package
          pip install south

        # add south to django settings.py's INSTALLED_APPS
          INSTALLED_APPS = (
              'django.contrib.admin',
              'django.contrib.auth',
              'django.contrib.contenttypes',
              'django.contrib.sessions',
              'django.contrib.messages',
              'django.contrib.staticfiles',
              'tastypie', # add tastypie package support
              'book',     # created by manage.py startapp book
              'article',
              'south', # add south package support
              'people',
          )

        # add a new app
          manage.py start app people

        # init new app migration schema file
          $ ./manage.py schemamigration people --initial

        # (option)if there are no south_migrationhistory in database then do this:
          $ ./manage.py syncdb

        # run migrate database
          $ ./manage.py migrate people

        # test django shell
          $ ./manage.py shell

        # test modify database table scheam, after run migrate or syncdb
          $ vim people/models.py  # then modify it's field defination.
          $ ./manage.py schemamigration people --auto  # build new schemamigration file
          $ ./manage.py migrate people  # after do this, the database people table will add a new field.


**Multi Database and Model Router Support**

    ::

        ref: https://docs.djangoproject.com/en/dev/topics/db/multi-db/

        # set settings.py add another database
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            },
            'scott': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'scott.sqlite3'),
            }
        }

        # run syncdb with --database=scott flag, it will build all tables of this project.
        ./manage.py syncdb --database=scott

        # test how to use multi database
        ./manage.py shell

        from book.models import first_book


        # query scott database
        first_book.objects.using('scott').all()
        
        # query default database
        first_book.objects.using('default').all()
        
        # query default database, too
        first_book.objects.all()


        # create record into scott database
        row=first_book(title=u'test for scott database')
        
        # save to scott database
        row.save(using='scott')

        # save to default database, you can run both up line and this line, it will save two record into two database.
        row.save(using='default')

        # save to default database
        row.save()


**Override Hydrate and Dehydrate method for create and read data**

    ::

        ref: https://github.com/toastdriven/django-tastypie/blob/master/tastypie/resources.py

        class first_book_resource(ModelResource):
            
            ...

            # Response data to client, 從 Django Model to Json 的過程會調用。可以用來增加欄位
            def dehydrate(self, bundle):
                bundle.data['custom_field'] = "Whatever you want"
                return bundle

            # Client send data to server, then you can modify and add some field you want. 可用來修改上傳的資料
            def hydrate(self, bundle):
                # import pdb;pdb.set_trace();
                # bundle.data[u'title']=u'scott modify data in hydrate method!'

                # defined field test
                bundle.data[u'body']=u'scott put test body content in hydrate method override!'

                # not extist field test, it will not raise error.
                bundle.data[u'test_field']=u'test field'

                return bundle


**SessionAuthentication & Django CSRF Token Access**

    ::

        ref: http://django-tastypie.readthedocs.org/en/latest/cookbook.html
        ref: https://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext

        0. check in Django Project settings.py and enable the CSRF Token Feature:
            MIDDLEWARE_CLASSES = (
                
                ...

                # if you want to use Tastypie Session Auth, you must enable this classess
                'django.middleware.csrf.CsrfViewMiddleware',

                ...

            )

            if this is disable, you can't use SessionAuthentication, because you can get CSRF Token String.

        1. First, you must login Django Admin System, and you will get a accessible permission CSRF Token.

        2. Body Tag Insert:
            {% csrf_token %}

        3. JQuery Ajax:
            $(document).ready(function() {
                // get list test session auth
                window.test_get_list_first_book_api=function(){
                    $.ajax({
                        url:'/api/first_book/?format=json',
                        type:'get',
                        contentType:'application/json',
                        success:function(res,status,xhr){
                            console.log(res);
                        },
                        beforeSend: function(jqXHR, settings) {
                            // Pull the token out of the DOM.
                            jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
                        },
                    });
                };
            });


**How to make user login in Server Side views.py**

    ::

        ref: https://docs.djangoproject.com/en/dev/topics/auth/default/#auth-web-requests

        #
        from django.contrib.auth import authenticate, login

        # 用來假設一個使用者執行登入, 這使系統管理員的帳號密碼
        def c_login(request):
            username = 'scott'
            password = '********'

            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponse('simulation do the admin login! after this, you can visite /admin URI.')


**Cookie and Session Operation**

    ::

        #
        # 基本上不使用 cookie 操作, 直接使用 Session 操作即可！
        #

        ref: https://docs.djangoproject.com/en/dev/topics/http/sessions/
        ref: http://stackoverflow.com/questions/17057536/how-to-set-cookie-in-django-and-then-render-template

        from django.http import HttpResponse

        def test(request):
            # import pdb;pdb.set_trace();

            try:print request.session['test']
            except:print 'request.session[\'test\'] is not existed!'
            
            # store new key-value in session to client
            request.session['test']='test'

            # build a response for cookie operation.    
            res=HttpResponse('Thanks for your comment!')

            # set cookie to client
            res.set_cookie(key='myKey', value='myValue')
            
            return res


**Install django-extensions**

    ::

        #
        # 提供類似 Rails 的 rake router, rake task 等多種功能(很讚!)
        #

        # 如果需要類似 rails 的 rake router 功能可以安裝此套件
        ref: https://github.com/django-extensions/django-extensions
        ref: http://django-extensions.readthedocs.org/en/latest/

        # install this package
            pip install django-extensions

        # add to settings.py

            INSTALLED_APPS = (
                
                ...

                'django_extensions',
            
                ...

            }

        # test it!

            ./manage.py  # show all function which you can do.

            ./manage.py show_urls


**Nested Resource 設計範例**

    ::

        # 參考：http://django-tastypie.readthedocs.org/en/latest/cookbook.html#nested-resources
        # 本案是調用 child_resource.get_detail(request, parent_id=obj.pk)
        # 亦可採用 child_resource.get_list(request, parent__id=obj.pk), 其關聯 Resource 的 relation_filter 要打開
        # 其中 .get_list 還要再稍微小做修改增加一個 filter Code 進去，利用 Django Relational QuerySet 來過濾出需要的資料。
        # 打開 relational filter: 
            class package_resource(ModelResource):
                    ...
                products = fields.ManyToManyField('nested.api.resource.product_resource', 'product_set', full=False)
                    ...
                class Meta:
                        ...
                    filtering = {
                        'package_name': 'exact gt gte lt lte',
                        # 打開 Django 的 Relational Model QuerySet Filter 規則給 ManyToMany 的 products 屬性。
                        'products': ALL_WITH_RELATIONS,
                    }
                        ...

        # urlpattern:
            # 加上有 product_resource 即可, 內部參考 cookbook 實做呼叫 package_resource
            url(r'^api6/', include(product_resource().urls)),

        # Sample Code:
            # 設定這個 API 回復的內容
            class package_resource(ModelResource):

                # 必須其中一個設定為 full = False, 將影響是展現 relation resource url 或是 object 資料
                # 千萬不可以兩個都設定為 full = True 會陷入無線迴圈！
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

                    import pdb;pdb.set_trace()

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


**Django Table Relation 設計範例**

    ::

        # 其實如果 Model 定義好了, 如果資料表不存在就 syncdb, 如果存在他就會使用現存資料表直接套用。
        # 所以對於已存在 Tables 的資料庫只要設定正確及可直接使用, 不需要在執行 syndb。

        class theF(models.Model):
            f = models.CharField(max_length=100, primary_key=True)
            label = models.TextField()
            mno = models.CharField(max_length=3, unique=True)

        class theG(models.Model):
            # 要設定為 IntegerField or AutoField 才會有 Auto increment 效果
            g = models.AutoField(max_length=100, primary_key=True)
            label = models.TextField()

            # 注意：將會自動幫你關聯與 relation model field 同樣的資料欄位型態
            # 簡單來說這個欄位也會被建立為 models.CharField(max_length=3, unique=True) 型態
            mno = models.ForeignKey('theF', to_field='mno', db_column='mno')


**models 放在 folder 內的技巧**

    ::

        # model_folder/models/__init__.py
            from .models import *

        # model_folder/models/models.py
            class theA(models.Model):
                a = models.CharField(max_length=100, primary_key=True)
                label = models.TextField()
                class Meta: 
                    app_label = 'model_folder'
                    # 參考 setting 內 install 的 app or app.path

            ...

        # settings.py

            INSTALLED_APPS = (
                ...
                'model_folder',
                ...
            )

            或上面全免直接設定 model 根目錄路徑：

            INSTALLED_APPS = (
                ...
                'model_folder.models',
                ...
            )


**Tastypie Resource Trace Work flow 解析備忘**

    ::

        # 概念上務必記得 request Query Paramater String 與 **kwargs 是分開的
            urlpattern 上的 parameter 將被帶入 **kwargs 內, 而且一定會被套用在該 meta.queryset 的 Model 上。
            而 request Query Paramater String 則只有在 get list 的時候會被在 update 近 **kwargs 內在該 meta.queryset 的 Model 上。

            所以可以確定 urlpattern 上的 parameter 只要按照 Django Relational Model 的 Filter 規則就能運作了, Resource 不大需要額外複寫什麼。

        # 總體來說, 所有 get 方法都會調用的方法, 差別只在於 detail 取 index[0]
            get_object_list

        # Tastypie Work Flow 的最後一個調用 Method = {restful verb}_{type} 命名
            
            get_list, get_detail, put_list, put_detail, patch_list, patch_detail, post_list(*)
                都會產生 create_response 給 client 端。

            delete_list, delete_details。
                不會有任何回應 HttpNoContent 就是沒有訊息還給 Client 的意思。

            post_detail(*)
                預設為 HttpNotImplemented。
                restful 好像沒有 post detail 這種不完整資料的方法。

        # details and list 之 filter 運作機制
            request query string 只有在 list 條件下會被轉為 kwargs 在套用到 Model 的 QuerySet.filter
            details 模式不會合併 query string 直接使用 url pattern 上的 parameter 做 QuerySet.filter

            參考 get_list > obj_get_list 內有一個
                # Update with the provided kwargs.
                filters.update(kwargs)

                # 參考 fiterings = { ... } 來把可以 filter 的關鍵字建立出來。
                # 將組合出符合 Django Model Relational Filter 的 Key-Value Dict
                applicable_filters = self.build_filters(filters=filters)

                # 透過這些 filters 將物件取出
                objects = self.apply_filters(bundle.request, applicable_filters)
                    apply_filters 會呼叫 get_object_list 再搭配 applicable_filters 做為 QuerySet 的 filter 參數。

**Tastypie Resource Mulitpart File Upload Deserializer**

    ::

        # 複寫 Resource 的 deserialize 方法增加 multipart 的支援即可！
        def deserialize(self, request, data, format=None):
            if not format:
                format = request.META.get('CONTENT_TYPE', 'application/json')

            # json 部分
            if format == 'application/x-www-form-urlencoded':
                return request.POST

            # mulitpart
            if format.startswith('multipart'):
                data = request.POST.copy()

                # 把 File fd 傳給 data dict 內作為 fd 的 Key-Value, 後面會傳給 Django Model ORM 轉入 Database
                # 似乎是使用 fd 物件(尚未 .read() ) 直接使用 __unicode__ 轉換擋名。
                data.update(request.FILES)

                # 注意：request.FILES 這個 fd 物件之的 __str__ 方法將 return fb charfield 該填寫的名稱
                # 然後 .read() 將返回 raw data
                # import pdb;pdb.set_trace()

                return data

**Tastypie 使用者認證的方法**

    ::

        # 通常會包含在存取資料過程中, 但是也可以單獨取出來用
        def dispatch(self, request_type, request, **kwargs):
                ...
            # 認證使用者, 成功後 request.user 將從 None 轉換為 User Instance
            # 無權限或是失敗會直接 response 回覆客戶端。
            # 預設採用 django Admin 的使用者權限設定！
            self.is_authenticated(request)
                ...
            return response


**Tastypie Resource 調用過程**

    ::

        # 按照 base_urls 內調要用

            dispatch_detail, dispatch_list
                ->

            dispatch
                快取節流
                允許方法 allowed_method
                使用者認證 self.is_authenticated
                檢查使用者權限
                取得下一個實做調用方法
                ->

            get_list, get_detail, post_list.....等等, return 為 create_response 返回客戶端。
                # 其內部調用
                    obj_get_list            # 內部會調用取得件的方法, Convert Request.GET to kwargs, combine kwargs & Request Query String, Authorization...
                    
                        build_filters       # according to _meta.filtering setting to rebuild Dict    
                                            # if this resource has a relation_set, need convert xxx_set__field -> xxx__field, and add it to Resource filtering Dict
                        
                        apply_filters       # 通常會調用 get_object_list(有些動作不會有這步), build a applicable_filters by filtering setting
                                            # apply with Django Filter Flow
                                            
                        get_object_list     # 真正從 QuerySet 取得 Model 物件的方法(全都有調用)
                    apply_sorting           # 預設資料排序
                    _meta.paginator_class   # 分頁
                    full_dehydrate          # 重購資料
                        dehydrate           # 可以複寫的重購方法
                        ->
                        
                        
**Tastypie Resource Relational Model Access**

    ::
    
        # override here
        def hydrate(self, bundle):
            if bundle.obj and bundle.obj.subscriber:
                subscriber = bundle.obj.subscriber
                subscriber.status = 'Audit'
    
                if 'mobile_device_id' in bundle.data:
                    subscriber.device_id = bundle.data.pop('mobile_device_id')
    
                if 'notification_method' in bundle.data:
                    subscriber.device_push_method = bundle.data.pop('notification_method')  # noqa
    
            return bundle
    
        # override here
        def save(self, bundle, skip_errors=False):
            bundle = super(SubscriberDataResource, self).save(bundle, skip_errors)
            bundle.obj.subscriber.save()
            return bundle
            

**Tastypie Custom Authorization**

    ::
    
        # ref: https://github.com/toastdriven/django-tastypie/blob/master/tastypie/authorization.py
        
        read_list
        read_detail
        create_list
        create_detail
        update_list
        update_detail
        delete_list
        delete_detail
        
