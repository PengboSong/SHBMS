from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from goods.models import Goods, Book


# 用户表
class Account(models.Model):
    type = ((1, "正常状态"), (2, "封禁中"), (3, '未激活'))
    type2 = ((1, "四平路校区"), (2, "嘉定校区"), (3, '闵行校区'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户名，密码，邮箱
    status = models.IntegerField(choices=type, default=1)
    business_account = models.BooleanField(default=False)
    school_num = models.IntegerField(unique=True)
    name = models.CharField(max_length=10, default='')
    school = models.IntegerField(choices=type2, default=1)
    phone = models.IntegerField()
    credit = models.IntegerField(default=90)

# 个人信息表
class PersonalInfo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(unique=True)
    mobile = models.DecimalField(max_digits=19, decimal_places=0)
    email = models.EmailField()

# 交易记录表
# order_time：交易创建时间，由用户自己上传，时间自动更新
# goods：由于此时商品已经下架，故不关联外键。直接用CharField类型记录达成交易商品名称
# seller，buyer：外键，关联用户
class TransRecord(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    goods = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)

# 留言表
# good_id:外键类型，关联商品表。方便用户通过留言查看对应商品内容
# from_id:外键，关联用户，表示留言人（买家）；to_id：外键类型，关联用户，表示被留言人（卖家）
# comment_time:留言创建时间
# short_content：为了避免有的用户留言过长，用此方式将超过30个字符内容显示为...，方便前端显示
class MessageRecord(models.Model):
    good_id = models.ForeignKey(Goods, on_delete=models.CASCADE)
    from_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    to_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False)
    picture = models.ImageField(upload_to='message_images', blank=True)

    def short_content(self):
        if len(str(self.content)) > 30:
            return '{}...'.format(str(self.content)[0:30])
        else:
            return str(self.content)
    short_content.allow_tags = True
