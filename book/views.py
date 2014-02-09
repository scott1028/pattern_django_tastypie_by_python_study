# coding: utf-8

from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse

def book_index(request):
    return TemplateResponse(request, 'index.html')#, {'entries': Entry.objects.all()})

#
from django.http import HttpResponse

def test(request):
	# import pdb;pdb.set_trace();
	# ref: https://docs.djangoproject.com/en/dev/topics/http/sessions/
	# ref: http://stackoverflow.com/questions/17057536/how-to-set-cookie-in-django-and-then-render-template

	try:print request.session['test']
	except:print 'request.session[\'test\'] is not existed!'
	
	# store new key-value in session to client
	request.session['test']='test'

	# build a response for cookie operation.	
	res=HttpResponse('Thanks for your comment!')

	# set cookie to client
	res.set_cookie(key='myKey', value='myValue')
	
	return res

from django.contrib.auth import authenticate, login

# 用來假設一個使用者執行登入, 這使系統管理員的帳號密碼
def c_login(request):
    username = 'scott'
    password = 't0036659'

    user = authenticate(username=username, password=password)
    login(request, user)

    return HttpResponse('simulation do the admin login! after this, you can visite /admin URI.')