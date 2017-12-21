from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Article,Category,Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","creat_time","last_time","category","author"]

admin.site.register(Article,ArticleAdmin)
admin.site.register((Category,Tag))