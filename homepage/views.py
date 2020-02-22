from django.http import HttpResponse
from django.shortcuts import render, redirect
from goods.models import Book, BookType
from django.contrib.auth.models import User
from django.contrib import auth


def homepage(request):
    types = BookType.objects.all()
    books = Book.objects.all()
    show_books = []
    for i in range(3):
        if books[i]:
            show_books.append(books[i])
        else:
            break
    context = {
        'types': types,
        'books': show_books,
    }

    return render(request, 'homepage.html', context)

def personal_center(request):
    return render(request, 'homepage.html', {})

def site_help(request):
    return render(request, 'help.html', {})

def search(request):
    book_name = request.POST.get('book_index', None)
    book_isbn = book_name
    context = {
        'books': Book.objects.filter(full_title=book_name),
        'books_isbn': Book.objects.filter(ISBN_num=book_isbn),
    }
    print(book_isbn)
    return render(request, 'books_with_index.html', context)


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    elif username:
        return render(request, 'error.html', {'message': '用户名或密码不正确'})
    else:
        return render(request, 'login.html')
