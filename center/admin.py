from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'name', 'credit',)
    search_fields = ('user', 'status', 'name', 'school', 'school_num',)
    raw_id_fields = ('user',)


class ViewAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'good_id', 'from_id', 'to_id', 'comment_time')
    search_fields = ('good_id', 'from_id', 'to_id')
    raw_id_fields = ('from_id', 'to_id', 'good_id')
    list_filter = ('to_id',)


class TransAdmin(admin.ModelAdmin):
    list_display = ( 'seller', 'buyer', 'order_time')
    search_fields = ('seller', 'buyer', 'goods')
    ordering = ('-order_time',)


admin.site.register(MessageRecord, ViewAdmin)
admin.site.register(TransRecord, TransAdmin)
admin.site.register(Account, AccountAdmin)

# Register your models here.
