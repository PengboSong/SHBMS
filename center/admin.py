from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


class ViewAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'good_id', 'from_id', 'to_id', 'comment_time')
    search_fields = ('good_id', 'from_id', 'to_id')
    raw_id_fields = ('from_id', 'to_id', 'good_id')
    list_filter = ('to_id',)


class TransAdmin(admin.ModelAdmin):
    list_display = ('goods', 'seller', 'costumer', 'order_time')
    search_fields = ('seller', 'costumer', 'goods')
    ordering = ('-order_time',)


admin.site.register(MessageRecord, ViewAdmin)
admin.site.register(TransRecord, TransAdmin)

# Register your models here.
