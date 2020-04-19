from django import forms
from .models import Account


class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = Account    #与models建立了依赖关系
        fields = {'school', 'phone'}
        labels = {
            'school': '学校',
            'phone': '电话',
        }
    email = forms.EmailField(label='邮箱')

