from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Goods, BookType
from . import form


def book_list(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book,
        'goods': Goods.objects.filter(book=book)
    }
    return render(request, 'book_detail.html', context)


def books_with_type(request, book_type_id):
    book_type = get_object_or_404(BookType, pk=book_type_id)
    context = {
        'books': Book.objects.filter(book_type=book_type),
        'book_type': book_type
    }
    return render(request, 'books_with_type.html', context)


def create_new_book(request):
    if request.method == "POST":
        obj = form.BookModelForm(request.POST)
        file_obj = request.FILES.get('pic')
        if obj.is_valid():
            post = obj.save(commit=False)
            post.picture = file_obj
            post.save()
            return HttpResponse("数据提交成功！！")
        else:
            return render(request, "create_new_book.html", {'obj': obj})
    else:
        obj = form.BookModelForm()
        return render(request, "create_new_book.html", {'obj': obj})


def up_shelf(request, book_id):
    book = Book.objects.filter(pk=book_id)
    if request.method == "POST":
        obj2 = form.GoodsModelForm(request.POST)
        file_obj_1 = request.FILES.get('pic1')
        file_obj_2 = request.FILES.get('pic2')
        if obj2.is_valid():
            post = obj2.save(commit=False)
            post.status = 1
            post.book = book[0]
            post.merchant = request.user
            post.picture_1 = file_obj_1
            post.picture_2 = file_obj_2
            post.save()
            return HttpResponse("数据提交成功！！")
        else:
            return render(request, "up_shelf.html", {'obj2': obj2, 'book': book[0]})
    else:
        obj2 = form.GoodsModelForm()
        return render(request, "up_shelf.html", {'obj2': obj2, 'book': book[0]})


# Create your views here.

