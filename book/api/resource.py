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

# 根據 Django-Admin 後台所題設定的使用者權限來驗證
# from tastypie.authorization import DjangoAuthorization
# 不需驗證使用者權限
from tastypie.authorization import Authorization

# 似乎預設的 Ajax 就是使用 content-type: application/x-www-form-urlencoded
import urlparse
class urlencodeSerializer(Serializer):

    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']

    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
    }

    # 實作轉換部分
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content):
        pass

# 設定這個 API 回復的內容
class first_book_resource(ModelResource):
    class Meta:
    	# 搜尋資料的依據
        queryset = first_book.objects.all()

        # 成為網址的 Resource
        resource_name = 'first_book'

        # 照抄 detail_allowed_methods=list_allowed_methods, 允許接受 Client Request 訪問的方法, 預設有 get 如果設定為 [] 將無法使用這個 Resource。
        list_allowed_methods = ['get', 'post', 'put', 'delete', 'patch'] # all support is default

        # (*)真正定義 Restful 支援的方法有哪些, 如果沒寫進去就伺服器就不支援(只需要設定這個即可)
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch'] # all support is default

        # 定義可以接受 Client Request Query String 的欄位與規則 ex: /api/first_book/?format=json&title=test
        filtering = {
    		'title': 'exact gt gte lt lte',
		}

		# 如果要製作 CRUD Restful API 必須在額外設定以下：資料序列化、用戶驗證、用戶權限(預設只有 ReadOnly)
		# 參考：http://django-tastypie.readthedocs.org/en/latest/resources.html#resource-options-aka-meta

        # 資料序列化, 如果要使用 Ajax Post 這邊要寫成這樣
        serializer = urlencodeSerializer()

        # 驗證用戶是誰(Authentication, BasicAuthentication, ApiKeyAuthentication, SessionAuthentication, DigestAuthentication, OAuthAuthentication, MultiAuthentication)
        authentication = Authentication()

        # 用戶的權限(Authorization, ReadOnlyAuthorization, DjangoAuthorization)
        authorization = Authorization()