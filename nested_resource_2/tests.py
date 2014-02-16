# coding:utf-8

from django.test import TestCase
from django.test import Client
import os

# for test database create a superuser
from django.contrib.auth.models import User

from django.core.files.uploadedfile import SimpleUploadedFile

from nested_resource_2.models import *

# Create your tests here.

class testNestedResource2(TestCase):
    def setUp(self):
        # Every test needs a client.

        # test data default is empty and need a super user for testing
        my_admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')

        # new a client
        self.client = Client()

        # Make user login
        self.client.login(username='admin', password='password')

        self.upload_file = open('manage.py','r')
        self.upload_file_fd = SimpleUploadedFile( self.upload_file.name, self.upload_file.read() )

        self.upload_file2 = open('README.rst','r')
        self.upload_file_fd2 = SimpleUploadedFile( self.upload_file2.name, self.upload_file2.read() )

    def test_post_data_to_theG(self):
        response = self.client.post('/admin/nested_resource_2/theg/add/', {'label':'test simulate client to post data into server' } )

    def test_upload_file_to_theE(self):

        # 測試保留 fd2 = null 上傳
        response = self.client.post('/admin/nested_resource_2/thee/add/', {
            'label':'test upload file fd & fd2',
            'fd': self.upload_file_fd2,
            # 'fd2': self.upload_file_fd2
        })

        # check it label name
        self.assertEqual(theE.objects.first().label, 'test upload file fd & fd2')

        # theE.objects.all()

        theE.objects.all().delete()

    def test_relaton_model(self):
        response = self.client.post('/theE_resource2/', {
            'label':'test upload file',
            'fd': self.upload_file_fd,
            'fd2':self.upload_file_fd
        })
        
        # check it label name
        self.assertEqual(theE.objects.first().label, 'test upload file')

        # theE.objects.all().delete()

        # import pdb;pdb.set_trace()

    def __del__(self):
        self.upload_file2.close()
        self.upload_file.close()
        print 'finalize...'