# coding: utf-8

from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login

#
from django.http import HttpResponse

# 用來假設一個使用者執行登入, 這使系統管理員的帳號密碼
def c_login(request):
    username = 'scott'
    password = 't0036659'

    user = authenticate(username=username, password=password)
    login(request, user)

    return HttpResponse('simulation do the admin login! after this, you can visite /admin URI.')

    # Create your views here.
from django.template.response import TemplateResponse

def index(request):
    return TemplateResponse(request, 'index.html')#, {'entries': Entry.objects.all()})