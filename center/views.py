from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import MessageRecord, TransRecord
from goods.models import Goods
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.models import User


def my_book(request, user_id):
    my_goods = Goods.objects.filter(merchant=user_id)
    context = {
        'my_goods': my_goods
    }
    return render(request, 'my_book.html', context)


def del_good(request, good_id):
    Goods.objects.filter(pk=good_id)[0].delete()
    return HttpResponse('删除成功')


def sell_good(request, good_id):
    target_good = Goods.objects.filter(id=good_id)[0]
    comments = MessageRecord.objects.filter(good_id=good_id)
    buyers = []
    for i in comments:
        buyers.append(i.from_id)
    context = {
        'target_good': target_good,
        'buyers': buyers,
    }
    if request.method == "POST":
        buyer_id = request.POST.get('buyer')
        TransRecord.objects.create(seller=request.user, goods=target_good.book.full_title, costumer=User.objects.filter(pk=int(buyer_id))[0], order_time=timezone.now(), price=target_good.price)
        Goods.objects.filter(id=good_id).update(status=3)

        return HttpResponse("商品卖出成功")
    elif target_good.status != 1:
        return HttpResponse('商品未上架，不能卖出。')
    else:
        return render(request, 'sell_good.html', context)


def personal_info(request, user_id):

    return HttpResponse('这里是个人信息')


def trans_info(request, user_id):
    trans_records = TransRecord.objects.filter(seller=request.user)
    buy_records = TransRecord.objects.filter(costumer=request.user)
    context = {
        'trans_records': trans_records,
        'buy_records': buy_records
    }
    return render(request, 'trans_record.html', context)


def personal_center(request, user_id):
    if request.user.id == user_id:
        return render(request, 'center.html', {})
    else:
        return HttpResponse("你没有权限访问该网页", status=404)


def my_comment(request, user_id):
    if request.user.id == user_id:
        my_comments = MessageRecord.objects.filter(to_id=user_id)
        context = {
            'my_comments': my_comments,
        }
        return render(request, 'my_comment.html', context)
    else:
        return HttpResponse("你没有权限访问该网页", status=404)


def reply(request, comment_id):
    comment = get_object_or_404(MessageRecord, pk=comment_id)
    good = comment.good_id
    from_id = request.user
    to_id = comment.from_id
    if request.method == "POST":
        view = request.POST.get('reply')
        MessageRecord.objects.create(content=view, from_id=from_id, to_id=to_id, good_id=good,
                                     comment_time=timezone.now)
        return HttpResponse('评论成功')
    else:
        return render(request, 'reply.html', {'comment':comment})
# Create your views here.
