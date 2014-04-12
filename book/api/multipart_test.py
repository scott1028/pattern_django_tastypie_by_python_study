# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import binascii
import re
import yaml

from django.conf import settings    # noqa
from django.core import serializers
from django.core.urlresolvers import reverse  # noqa
from django.conf.urls import patterns, url  # noqa
from django.db.models import Q  # noqa
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from tastypie import authentication
from tastypie import exceptions
from tastypie import fields
from tastypie import http
from tastypie import utils
from django.contrib.auth.models import User

from tastypie.constants import ALL, ALL_WITH_RELATIONS  # noqa
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse, Unauthorized  # noqa
from tastypie.resources import ModelResource
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash  # noqa


BATCH_PATTERN = r'^(\w+):\s+\"?(\w+)\"?'


class MultipartResourceMixin(object):
    def _patch_request_body_property(self, request):
        if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
            request.__class__.body = None

    def dispatch(self, request_type, request, **kwargs):
        self._patch_request_body_property(request)
        return super(MultipartResourceMixin, self).dispatch(request_type,
                                                   request, **kwargs)

    def deserialize(self, request, data, format='application/json'):
        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)

            return data

        return super(MultipartResourceMixin, self).deserialize(
            request,
            data,
            format
        )

class upload(ModelResource, MultipartResourceMixin):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'upload'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        excludes = [
            'update_date',
            'create_date',
            'expire_date',
            'pk'
        ]

    def post_list(self, request, **kwargs):
        print (request.body)
        data = self.deserialize(
            request, request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json'))

        return http.HttpCreated()

    def deserialize(self, request, data, format='application/json'):
        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data

        return super(upload, self).deserialize(
            request,
            data,
            format
        )

class upload_query(ModelResource, MultipartResourceMixin):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'upload_query'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        excludes = [
            'update_date',
            'create_date',
            'expire_date',
            'pk'
        ]

    def post_list(self, request, **kwargs):
        print (request.body)
        data = self.deserialize(
            request, request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json'))

        return http.HttpCreated()

