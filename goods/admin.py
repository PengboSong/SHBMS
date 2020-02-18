from django.contrib import admin
from .models import *


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'price', 'status', 'merchant')
    ordering = ('id',)
    search_fields = ('id', 'book', 'status')
    list_filter = ('status', 'book', 'merchant')


class BookAdmin(admin.ModelAdmin):
    list_display = ('full_title', 'authors', 'original_price')
    search_fields = ('full_title', 'id')


admin.site.register(Goods, GoodsAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookType, TypeAdmin)
# Register your models here.
