from django.test import TestCase
from django.test import Client
import os

# for test database create a superuser
from django.contrib.auth.models import User

from django.core.files.uploadedfile import SimpleUploadedFile

from nested_resource_2.models import *

# Create your tests here.

class testTheE(TestCase):
    def setUp(self):
        # Every test needs a client.

        # test data default is empty and need a super user for testing
        my_admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')

        # new a client
        self.client = Client()

        # Make user login
        self.client.login(username='admin', password='password')

    def test_post_data_to_theG(self):
        response = self.client.post('/admin/nested_resource_2/theg/add/', {'label':'test simulate client to post data into server' } )

    def test_upload_file_to_theE(self):
        upload_file = open('manage.py','r')
        response = self.client.post('/admin/nested_resource_2/thee/add/', {'label':'test upload file', 'fd': SimpleUploadedFile(upload_file.name, upload_file.read()) } )

        # check it label name
        self.assertEqual(theE.objects.first().label, 'test upload file')
