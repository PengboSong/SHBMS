from django.db import models
from django.contrib.auth.models import User


class MyChar(models.Field):
    def __init__(self, max_length, unique, *args, **kwargs):
        self.max_length = max_length
        super(MyChar, self).__init__(max_length=max_length, unique=unique, *args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % self.max_length
# 自定义数据（char）


class BookType(models.Model):

    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

# 书籍类型表


class Book(models.Model):
    book_type = models.ForeignKey(BookType, on_delete=models.DO_NOTHING)
    full_title = models.CharField(max_length=255)
    ISBN_num = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='books_images')
    original_price = models.DecimalField(max_digits=19, decimal_places=2)
# 书籍信息表


class Goods(models.Model):
    type = ((1, "上架中"), (2, "待处理"), (3, "已下架") )
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    description = models.TextField(blank=False)
    picture_1 = models.ImageField(upload_to='goods_images', blank=False)
    picture_2 = models.ImageField(upload_to='goods_images', blank=True)
    status = models.IntegerField(choices=type)
# 商品表

# Create your models here.
