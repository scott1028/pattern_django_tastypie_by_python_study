# coding:utf-8

__author__ = 'scott'

from tastypie import fields

from tastypie.resources import ModelResource
from django.contrib.auth.models import Group,User,Permission

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