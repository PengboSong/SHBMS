from django.db import models
from django.contrib.auth.models import User


# 自定义数据（char）
# 由于models里没有char数据类型，所以选择用自定义类来实现
class MyChar(models.Field):
    def __init__(self, max_length, unique, *args, **kwargs):
        self.max_length = max_length
        super(MyChar, self).__init__(max_length=max_length, unique=unique, *args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % self.max_length


# 书籍类型表
# 为了方便根据书籍的类型标签索引和后台管理，将书籍类型单独拿出创建一类
class BookType(models.Model):

    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


# 书籍信息表
# book_type变量，外键对应书籍类型表；
# 校园二手书交易特点：对某本特定书籍的买卖需求量很大，所以建立书籍表方便对某本特定书籍进行操作
class Book(models.Model):
    status = ((1, "上架中"), (2, "待处理"), (3, "已下架"))
    book_status = models.IntegerField(choices=status, default=2)
    book_type = models.ForeignKey(BookType, on_delete=models.DO_NOTHING)
    full_title = models.CharField(max_length=255)
    ISBN_num = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='books_images')
    original_price = models.DecimalField(max_digits=19, decimal_places=2)


# 商品表
# 变量status：显示商品状态。默认上架，当用户选择下架商品或卖出商品后状态为下架，当用户被封禁，再次尝试登录时该用户卖的商品自动下架
# 变量book：外键，关联Book表，建立对应关系后，用户只需填写价格，描述，图片就可上架商品，大大简化了上架流程
# 变量merchant：外键，关联用户表。在上架商品时系统自动调用登录用户作为merchant的值
# 变量picture_1:图片文件，用于展示商品特征（必填）；picture_2:选填
class Goods(models.Model):
    type = ((1, "上架中"), (2, "待处理"), (3, "已下架") )
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    description = models.TextField(blank=False)
    picture_1 = models.ImageField(upload_to='goods_images', blank=False)
    picture_2 = models.ImageField(upload_to='goods_images', blank=True)
    status = models.IntegerField(choices=type)


# Create your models here.
