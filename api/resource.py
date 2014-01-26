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
    # pass

    def get_list(self, request, **kwargs):
        # this is override method
        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
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