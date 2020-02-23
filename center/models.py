from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from goods.models import Goods


# 用户表
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    business_account = models.BooleanField(default=False)

# 个人信息表
class PersonalInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(unique=True)
    mobile = models.DecimalField(max_digits=19, decimal_places=0)
    email = models.EmailField()

# 交易记录表
class TransRecord(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    costumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='costumer')
    goods = models.CharField(max_length=255)
    order_time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)

# 留言表
class MessageRecord(models.Model):
    good_id = models.ForeignKey(Goods, on_delete=models.CASCADE)
    from_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    to_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False)

    def short_content(self):
        if len(str(self.content)) > 30:
            return '{}...'.format(str(self.content)[0:30])
        else:
            return str(self.content)
    short_content.allow_tags = True
