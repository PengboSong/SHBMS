from random import Random # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from .models import EmailVerifyRecord  # 邮箱验证model
from SHBMS.settings import EMAIL_FROM  # setting.py添加的的配置信息
# 生成随机字符串


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.save()
    email_title = "注册激活"
    email_body = "验证码："+code
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass


