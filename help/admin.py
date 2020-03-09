from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'comment_time')
    ordering = ('-comment_time',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Notice, NoticeAdmin)
