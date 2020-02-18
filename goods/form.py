from django import forms
from . import models


class BookModelForm(forms.ModelForm):
    class Meta:
        model = models.Book    #与models建立了依赖关系
        fields = {'book_type', 'full_title', 'ISBN_num', 'publisher', 'authors', 'original_price'}
        labels = {
            'book_type': '类型',
            'full_title': '标题',
            'ISBN_num': 'isbn',
            'publisher': '出版社',
            'authors': '作者',
            'original_price': '原价',
        }


class GoodsModelForm(forms.ModelForm):
    class Meta:
        model = models.Goods
        fields = {'price', 'description'}
        labels = {
            'price': '上架价格',
            'description': '商品描述',
        }

