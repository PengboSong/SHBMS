from django.shortcuts import render
from django.http import HttpResponse
from .models import MessageRecord
from goods.models import Goods
from django.http import Http404
from django.contrib.auth.models import User


def my_book(request, user_id):
    my_goods = Goods.objects.filter(merchant=user_id)
    context = {
        'my_goods': my_goods
    }
    return render(request, 'my_book.html', context)


def personal_info(request, user_id):

    return HttpResponse('这里是个人信息')


def trans_info(request, user_id):
    return HttpResponse('这里是交易记录')


def personal_center(request, user_id):
    if request.user.id == user_id:
        return render(request, 'center.html', {})
    else:
        return HttpResponse("你没有权限访问该网页", status=404)


def comment(request, user_id):
    if request.user.id == user_id:
        my_comments = MessageRecord.objects.filter(to_id=user_id)
        context = {
            'my_comments': my_comments,
        }
        return render(request, 'comment.html', context)
    else:
        return HttpResponse("你没有权限访问该网页", status=404)


# Create your views here.
