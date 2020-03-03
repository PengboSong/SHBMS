from django import forms
from center.models import Account


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account   #与models建立了依赖关系
        fields = {'school_num', 'name', 'school', 'phone'}
        labels = {
            'school_num': '学号',
            'name': '真实姓名',
            'school': '校区',
            'phone': '联系方式',
        }

    username = forms.CharField(
        max_length=10,
        error_messages={'max_length': '用户名太长了（2-16字符）', 'required': '用户名不能为空'},
        label='用户名',
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={'required': '密码不能为空'},
        label='密码',
    )
    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '与上面密码保持一致'}),
        error_messages={'required': '密码不能为空'},
        label='重复密码',
    )
    email = forms.EmailField(label='邮箱')

