# coding:utf-8
# resource api sample.

from tastypie.resources import Resource
from tastypie import fields
 
class dict2obj(object):
    """
    Convert dictionary to object
    @source http://stackoverflow.com/a/1305561/383912
    """
    def __init__(self, d):
        self.__dict__['d'] = d
 
    def __getattr__(self, key):
        value = self.__dict__['d'][key]
        if type(value) == type({}):
            return dict2obj(value)
 
        return value
 
class multi_resource(Resource):
    title = fields.CharField(attribute='title')
    content = fields.CharField(attribute='content')
    author = fields.CharField(attribute='author_name')
 
    class Meta:
        resource_name = 'test'
 
    def obj_get_list(self, request=None, **kwargs):
 
        posts = []
        #your actual logic to retrieve contents from external source.
 
        #example
        posts.append(dict2obj(
            {
                'title': 'Test Blog Title 1',
                'content': 'Blog Content',
                'author_name': 'User 1'
            }
        ))
        posts.append(dict2obj(
            {
                'title': 'Test Blog Title 2',
                'content': 'Blog Content 2',
                'author_name': 'User 2'
            }
        ))
 
        return posts

    # 參考：http://django-tastypie.readthedocs.org/en/latest/resources.html#dehydrate-foo
    def dehydrate_title(self,bundle):
        return bundle.data['title'].upper()