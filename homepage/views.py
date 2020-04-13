from django.shortcuts import render, redirect, get_object_or_404
from goods.models import Book, BookType
from center.models import TransRecord, Account
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from . import forms


# 用于将一个书籍列表按销量取出top3
# 销量来源：交易记录
# 此方法避免了书籍列表为空时的报错
def sort_book(book_list):
    all_tans = TransRecord.objects.all()
    num_list = []
    for book in book_list:
        if book:
            buy_num = 0
            for tran in all_tans:
                if tran.goods == book:
                    buy_num = buy_num + 1
            num_list.append((buy_num, book.pk))
    length = len(num_list)
    if length > 3:
        length = 3
    sorted(num_list)
    show_books = []
    for i in range(length):
        if num_list[i]:
            show_books.append(get_object_or_404(Book, pk=num_list[i][1]))
        else:
            break
    return show_books


# 主页：内含所有书籍销量top3和书籍按类型分类各类型top3
def homepage(request):
    types = BookType.objects.all()
    books = Book.objects.filter(book_status=1)
    show_all_books = sort_book(books)
    context = {
        'types': types,
        'books': show_all_books,
    }
    for i in range(1, 13):
        book_type = BookType.objects.filter(pk=i)[0]
        book_with_type = Book.objects.filter(book_type=book_type)
        show_book_type = sort_book(book_with_type)
        context[book_type.type_name] = show_book_type

    return render(request, 'homepage.html', context)


# 搜索界面，可以按照isbn编号或者书本标题进行搜索
def search(request):
    book_index = request.POST.get('book_index', None)
    context = {
        'books': Book.objects.filter(Q(full_title=book_index) | Q(ISBN_num=book_index) & Q(book_status=1))
    }
    return render(request, 'books_with_index.html', context)


# 登录界面，若用户未登录则禁止进入网页
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    elif username:
        return render(request, 'login.html', {'message': '用户名或密码不正确'})
    else:
        return render(request, 'login.html', {})


# Create your views here.
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
                print(password + re_password)
                error = '两次密码输入不一致'
                return render(request, 'register.html', {'obj': obj, 'message': error})
            else:
                post = obj.save(commit=False)
                post.status = 1
                post.user = user
                post.save()
                return redirect('/')
        else:
            return render(request, 'register.html', context={'message': error, 'obj': obj})
    else:
        obj = forms.AccountModelForm()
        return render(request, 'register.html', {'obj': obj})


