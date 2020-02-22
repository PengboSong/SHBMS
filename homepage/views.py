from django.http import HttpResponse
from django.shortcuts import render
from goods.models import Book


def homepage(request):
    return render(request, 'index.html', {})

def explore(request):
    return render(request, 'explore.html', {})

def center(request):
    return render(request, 'personal_center.html', {})

def site_help(request):
    return render(request, 'help.html', {})


def site_introduce(request):
    pass

def search(request):
    book_name = request.POST.get('book_index', None)
    book_isbn = book_name
    context = {
        'books': Book.objects.filter(full_title=book_name),
        'books_isbn': Book.objects.filter(ISBN_num=book_isbn),
    }
    print(book_isbn)
    return render(request, 'books_with_index.html', context)
