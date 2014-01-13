# coding:utf-8

from django.contrib import admin

# Register your models here.
from book.models import first_book
from django.utils.html import format_html

class bookAdmin(admin.ModelAdmin):

	# actions_on_bottom=True

	date_hierarchy = 'pub_date'

	fields=(('title','pub_date'),'body')

	list_display=['title','pub_date','my_customize_field']

	# 自行增加欄位, 可以用來客製化圖表列表等
	def my_customize_field(self,obj):
		return format_html('<img src="/%s">'%(obj.title))

	pass

admin.site.register(first_book,bookAdmin)