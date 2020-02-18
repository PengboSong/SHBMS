from django.http import HttpResponse
from django.shortcuts import render
from goods.models import Book


def homepage(request):
    return render(request, 'homepage.html', {})


def center(request):
    return HttpResponse('这里是个人中心')


def site_help(request):
    return HttpResponse('这里是帮助中心')


def site_introduce(request):
    return HttpResponse('这里是网页详情页')


def search(request):
    book_name = request.POST.get('book_index', None)
    book_isbn = book_name
    context = {
        'books': Book.objects.filter(full_title=book_name),
        'books_isbn': Book.objects.filter(ISBN_num=book_isbn),
    }
    print(book_isbn)
    return render(request, 'books_with_index.html', context)


# Create your views here.
