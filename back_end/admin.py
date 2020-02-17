from django.contrib import admin
from.models import Goods


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_id', 'price', 'description', 'status')
    ordering = 'id'


admin.site.register(Goods)
# Register your models here.
