# coding:utf-8

from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from public.models import *

# 設定這個 API 回復的內容
class public(ModelResource):
    # product_id = fields.CharField(attribute='product__product_id', null=True)  # 會受到 db_constraint 影響找不到物件會返還 404
    product_id = fields.CharField(attribute='product_id')  # 不會受到 db_constrains 影響

    # MNO.objects.filter(product__product_id__contains='a9')

    # 似乎無法使用真實值來做 Filter
    # MNO.objects.filter(product_id__contains='a9')
    # raise TypeError('Related Field got invalid lookup: %s' % lookup_type)

    # product_id2 = fields.CharField(attribute='product__product_id', null=True, default='', blank=True)
    class Meta:
        queryset = MNO.objects.all()
        resource_name = 'mno'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            "product_id": ALL,
            "product_id2": ALL,
        }
