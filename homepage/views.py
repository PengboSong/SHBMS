from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.views.generic.base import TemplateView

from . import forms, send_email, models
from .models import EmailVerifyRecord
from goods.models import Book, BookType
from center.models import TransRecord, Account


# 用于将一个书籍列表按销量取出top3
# 销量来源：交易记录
# 此方法避免了书籍列表为空时的报错
def sort_book(book_list):
    sale_stat = [(book.sale_volume, book.pk) for book in book_list]
    sale_stat.sort(key=lambda x: x[0], reverse=True)
    top3_books = [get_object_or_404(Book, pk=item[1]) for item in sale_stat][:3]
    return top3_books

# 主页：内含所有书籍销量top3和书籍按类型分类各类型top3
class HomePageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_types = BookType.objects.all()
        books = Book.objects.filter(book_status=1)
        books_in_order = sort_book(books)

        sub_categories = [
            {
                "name": "理工类",
                "list": {
                    1: "理学",
                    2: "医学",
                    3: "计算机",
                    4: "工学",
                    7: "经济管理",
                    13: "农学",
                }
            },
            {
                "name": "人文艺术类",
                "list": {
                    5: "人文",
                    6: "法律",
                    8: "语言学",
                    9: "心理",
                    10: "哲学",
                    11: "艺术",
                    12: "教育",
                }
            },
            {
                "name": "其他",
                "list": {
                    14: "小说",
                    15: "散文",
                    16: "诗歌",
                    17: "其他",
                }
            }
        ]

        context['sub_categories'] = sub_categories
        context['book_types'] = book_types
        context['book_type_names'] = [book_type.type_name for book_type in book_types]
        context['top_books'] = sort_book(Book.objects.all())
        for book_type in book_types:
            book_with_type = Book.objects.filter(Q(book_type=book_type) & Q(book_status=1))
            context[book_type.type_name] = sort_book(book_with_type)
        return context

# 搜索界面，可以按照isbn编号或者书本标题进行搜索
def search(request):
    book_index = request.POST.get('book_index', None)
    context = {
        'books': Book.objects.filter(Q(full_title=book_index) | Q(ISBN_num=book_index) & Q(book_status=1))
    }
    return render(request, 'books_with_index.html', context)

# 登录界面，若用户未登录则禁止进入网页
class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        username = request.POST.get('username', '')
        if not username:
            messages.warning(self.request, "用户名不能为空")
            return self.render_to_response(context)

        password = request.POST.get('password', '')
        if not password:
            messages.warning(self.request, "密码不能为空")
            return self.render_to_response(context)
        
        user = auth.authenticate(request, username=username, password=password)
        if user is None:
            messages.error(self.request, "用户名或密码不正确")
        else:
            auth.login(request, user)
            return redirect('/')

def logout(request):
    auth.logout(request)
    return HttpResponse('登出成功')

class RegisterView(TemplateView):
    template_name = "register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj"] = forms.AccountModelForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        obj = forms.AccountModelForm(request.POST)
        context["obj"] = obj
        if obj.is_valid():
            username = obj.cleaned_data['username']
            password = obj.cleaned_data['password']
            re_password = obj.cleaned_data['re_password']
            email = obj.cleaned_data['email']

            if User.objects.filter(username=username):
                messages.error(request, "用户名已存在")
                return self.render_to_response(context)
            
            if password != re_password:
                messages.error(request, "两次密码输入不一致")
                return self.render_to_response(context)
            
            user = User.objects.create(username=username, password=make_password(password), email=email)
            post_obj = obj.save(commit=False)
            post_obj.status = 1
            post_obj.user = user
            post_obj.save()
            return redirect('/')


def check_email(request):
    if request.method == 'POST':
        school_num = request.POST.get('school_num')
        check_user = Account.objects.filter(school_num=int(school_num))
        if check_user:
            user = check_user[0].user
            send_email.send_register_email(user.email)
            record = EmailVerifyRecord.objects.filter(code=active_code)
            if record:
                record[0].delete()
                return render(request, 'send_email.html', {'id': user.pk})
            else:
                return render(request, 'send_email.html', {'msg': '验证码输入错误'})
        else:
            return render(request, 'send_email.html', {'msg': '用户不存在'})
    else:
        return render(request, 'send_email.html')


class UpdatePasswordView(TemplateView):
    template_name = "update_password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj"] = forms.AccountModelForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        obj = forms.AccountModelForm(self.request.POST)
        context["obj"] = obj
        user_id = context["user_id"]
        password = obj.cleaned_data['password']
        re_password = obj.cleaned_data['re_password']

        if password != re_password:
            messages.error(request, "两次密码输入不一致")
            return self.render_to_response(context)
            
        User.objects.filter(id=user_id).update(password=password)
        return redirect('/')
