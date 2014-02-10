# coding:utf-8
# resource api sample.

from tastypie.resources import Resource
from tastypie import fields

class virtualModel(object):
    def __init__(self, mno=None):
        self._mno = mno

    @property
    def mno_name(self):
        return self._mno.name

    @property
    def balance_query_code(self):
        return 'balance_query_code'

    @property
    def cca_code(self):
        return 'cca_code'

    @property
    def apn(self):
        return 'apn'

class multi_resource(Resource):
    title = fields.CharField(attribute='title')
    content = fields.CharField(attribute='content')
    author = fields.CharField(attribute='author_name')
 
    class Meta:
        object_class = virtualModel
        resource_name = 'test'
 
    def obj_get_list(self, bundle, **kwargs):
        # import pdb;pdb.set_trace()

        return []

    # 參考：http://django-tastypie.readthedocs.org/en/latest/resources.html#dehydrate-foo
    def dehydrate_title(self,bundle):
        return bundle.data['title'].upper()