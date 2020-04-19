from django.shortcuts import render, redirect, get_object_or_404
from goods.models import Book, BookType
from center.models import TransRecord, Account
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from . import forms, send_email, models
from .models import EmailVerifyRecord
from django.contrib import messages
from django.views.generic.base import TemplateView


# 用于将一个书籍列表按销量取出top3
# 销量来源：交易记录
# 此方法避免了书籍列表为空时的报错
def sort_book(book_list):
    sale_num = []
    show_books = []
    for book in book_list:
        sale_num.append((book.sale_volume, book.pk))
    sorted(sale_num)
    i = 0
    for show_book in sale_num:
        if show_book and i < 3:
            show_books.append(get_object_or_404(Book, pk=show_book[1]))
            i = i+1
    return show_books

# 主页：内含所有书籍销量top3和书籍按类型分类各类型top3
class HomePageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_types = BookType.objects.all()
        books = Book.objects.filter(book_status=1)
        books_in_order = sort_book(books)

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        if (username is None) or (password is None):
            messages.warning(self.request, "用户名或密码不能为空")
            return self.render_to_response()
        else:
            user = auth.authenticate(request, username=username, password=password)
            if user is None:
                messages.error(self.request, "用户名或密码不正确")
            else:
                auth.login(request, user)
                return redirect('/')

# def login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     if (username is not None) and (password is not None):
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             return render(request, 'login.html', {'message': '用户名或密码不正确'})
#     else:
#         return render(request, 'login.html', {})

def logout(request):
    auth.logout(request)
    return HttpResponse('登出成功')

def register(request):
    if request.method == 'POST':
        obj = forms.AccountModelForm(request.POST)
        error = ''
        if obj.is_valid():
            username = obj.cleaned_data['username']
            password = obj.cleaned_data['password']
            re_password = obj.cleaned_data['re_password']
            email = obj.cleaned_data['email']
            if User.objects.filter(username=username):
                error = '已存在的用户名'
                return render(request, 'register.html', {'obj': obj, 'message': error})
            else:
                user = User.objects.create(username=username, password=make_password(password), email=email)
            if password != re_password:
                error = '两次密码输入不一致'
                return render(request, 'register.html', {'obj': obj, 'message': error})
            else:
                post = obj.save(commit=False)
                post.status = 1
                post.user = user
                post.save()
                return redirect('/')
        else:
            return render(request, 'register.html', context={'obj': obj})
    else:
        obj = forms.AccountModelForm()
        return render(request, 'register.html', {'obj': obj})


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


def update_password(request, user_id):
    if request.method == 'POST':
        obj = forms.PasswordForm(request.POST)
        password = obj.cleaned_data['password']
        re_password = obj.cleaned_data['re_password']
        if password != re_password:
            error = '两次密码输入不一致'
            return render(request, 'update_password.html', {'obj': obj, 'message': error})
        else:
            User.objects.filter(id=user_id).update(password=password)
            redirect('/')
    else:
        obj = forms.PasswordForm(request.POST)
        return render(request, 'update_password.html', {'obj': obj})
