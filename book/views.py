from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse

def book_index(request):
    return TemplateResponse(request, 'index.html')#, {'entries': Entry.objects.all()})
