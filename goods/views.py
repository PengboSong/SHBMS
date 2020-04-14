from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Goods, BookType
from . import form
from django.db.models import Q
from django.utils import timezone
from center.models import MessageRecord, TransRecord, Account
from django.contrib.auth.models import User


def book_list(request):
    books = Book.objects.filter(book_status=1)
    context = {
        'books': books
    }
    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book': book,
        'goods': Goods.objects.filter(Q(book=book) & Q(status=1))
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
            post.status = 2
            post.save()
            return HttpResponse("数据提交成功,正在等待审核，审核通过后即可上架")
        else:
            return render(request, "create_new_book.html", {'obj': obj})
    else:
        if get_object_or_404(Account, user=request.user).status == 1:
            obj = form.BookModelForm()
            return render(request, "create_new_book.html", {'obj': obj})
        else:
            return HttpResponse('您无权限进行此操作')


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
        if get_object_or_404(Account, user=request.user).status == 1:
            obj2 = form.GoodsModelForm()
            return render(request, "up_shelf.html", {'obj2': obj2, 'book': book[0]})
        else:
            return HttpResponse('您无权限进行此操作')


def good_detail(request, good_id):
    good = Goods.objects.filter(pk=good_id)[0]
    sell_book = TransRecord.objects.filter(seller=request.user)
    sell_num = len(sell_book)
    credit_point = get_object_or_404(Account, user=request.user).credit
    return render(request, "good_detail.html", {'good': good, 'sell_num': sell_num, 'credit_point': credit_point})


def comment(request, good_id):
    good = get_object_or_404(Goods, pk=good_id)
    context = {
        'good': good
    }
    if request.method == "POST":
        view = request.POST.get('comment')
        MessageRecord.objects.create(content=view, from_id=request.user, to_id=good.merchant, good_id=good, comment_time=timezone.now)
        return HttpResponse('评论成功')
    else:
        if get_object_or_404(Account, user=request.user).status == 1:
            return render(request, 'comment.html', context)
        else:
            return HttpResponse('您无权限进行此操作')


# Create your views here.

