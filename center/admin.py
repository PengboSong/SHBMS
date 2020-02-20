from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


class ViewAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'good_id', 'from_id', 'to_id', 'comment_time')
    search_fields = ('good_id', 'from_id', 'to_id')


admin.site.register(MessageRecord, ViewAdmin)

# Register your models here.
