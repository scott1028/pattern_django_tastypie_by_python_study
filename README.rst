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

        # 如果需要類似 rails 的 rake router 功能可以安裝此套件
        ref: https://github.com/django-extensions/django-extensions

        # install this package
            pip install django-extensions

        # add to settings.py

            INSTALLED_APPS = (
                
                ...

                'django_extensions',
            
                ...

            }

        # test it!

            ./manage.py show_urls


