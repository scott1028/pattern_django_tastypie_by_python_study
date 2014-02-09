# coding: utf-8

from django.shortcuts import render

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