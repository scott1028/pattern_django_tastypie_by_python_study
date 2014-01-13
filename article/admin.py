from django.contrib import admin

# Register your models here.
from article.models import Article,Reporter
from django.utils.html import format_html

class articleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article,articleAdmin)

class reporterAdmin(admin.ModelAdmin):
	pass

admin.site.register(Reporter,reporterAdmin)