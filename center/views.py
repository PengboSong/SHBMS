from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import MessageRecord, TransRecord, Account
from goods.models import Goods, Book
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from . import form


def personal_center(request, user_id):
    if request.user.is_authenticated and request.user.pk == user_id:
        my_goods = Goods.objects.filter(merchant=user_id)
        trans_records = TransRecord.objects.filter(Q(seller=request.user) | Q(buyer=request.user))
        trans_3_record = []
        context={}
        length = len(my_goods)
        if length > 3:
            length = 3
        for i in range(length):
            context[str(i)] = my_goods[i]
        length = len(trans_records)
        if length > 3:
            length = 3
        for j in range(length):
            trans_3_record.append(trans_records[j])
        context['trans_records'] = trans_3_record
        return render(request, 'center.html', context)
    else:
        return HttpResponse('您无权限访问该网页')


def my_book(request, user_id):
    my_goods = Goods.objects.filter(merchant=user_id)
    context = {
        'my_goods': my_goods
    }
    if request.user.is_authenticated and request.user.pk == user_id:
        return render(request, 'my_book.html', context)
    else:
        return HttpResponse('您无权限访问该网页')


def del_good(request, good_id):
    if get_object_or_404(Account, user=request.user).status == 1:
        Goods.objects.filter(pk=good_id)[0].delete()

        return HttpResponse('删除成功')
    else:
        return HttpResponse('您无权限进行该操作')


def sell_good(request, good_id):
    if get_object_or_404(Account, user=request.user).status == 1:
        target_good = Goods.objects.filter(id=good_id)[0]
        cur_volume = Book.objects.get(id=target_good.book.pk).sale_volume+1
        cur_credit = Account.objects.get(user=request.user).credit+5
        comments = MessageRecord.objects.filter(good_id=good_id)
        buyers = []
        for i in comments:
            buyers.append(i.from_id)
        context = {
            'target_good': target_good,
            'buyers': buyers,
        }
        if request.method == "POST":
            buyers_id = request.POST.get('buyer')
            TransRecord.objects.create(seller=request.user, goods=target_good.book, buyer=User.objects.filter(pk=int(buyers_id))[0], order_time=timezone.now(), price=target_good.price)
            Book.objects.filter(id=target_good.book.pk).update(sale_volume=cur_volume)
            Goods.objects.filter(pk=good_id).update(status=3)
            Account.objects.filter(user=request.user).update(credit=cur_credit)
            return HttpResponse("商品卖出成功")
        elif target_good.status != 1:
            return HttpResponse('商品未上架，不能卖出。')
        else:
            return render(request, 'sell_good.html', context)
    else:
        return HttpResponse('您无权限进行该操作')


def personal_info(request, user_id):
    if request.user.is_authenticated and request.user.pk == user_id:
        my_account = get_object_or_404(Account,user=request.user)
        context = {
        'my_account': my_account
        }
        return render(request, 'personal_info.html', context)
    else:
        return HttpResponse('您无权限访问该网页')


def update_info(request, user_id):
    if request.user.pk == user_id:
        my_account = get_object_or_404(Account, user=request.user)
        if request.method == "POST":
            obj = form.UpdateInfoForm(request.POST)
            if obj.is_valid():
                User.objects.filter(pk=user_id).update(email=obj.cleaned_data['email'])
                Account.objects.filter(user=request.user).update(phone=obj.cleaned_data['phone'],
                                                                school=obj.cleaned_data['school'])

                return HttpResponse('修改成功')
        else:
            obj = form.UpdateInfoForm(request.POST)
            return render(request, 'update_info.html',{'my_account': my_account, 'obj': obj})
    else:
        return HttpResponse('您无权限访问该网页')


def trans_info(request, user_id):
    trans_records = TransRecord.objects.filter(seller=request.user)
    buy_records = TransRecord.objects.filter(buyer=request.user)
    context = {
        'trans_records': trans_records,
        'buy_records': buy_records
    }
    if request.user.pk == user_id:
        return render(request, 'trans_record.html', context)
    else:
        return HttpResponse('您无权限访问该网页')


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
        pic = request.POST.get('pic')
        MessageRecord.objects.create(content=view, from_id=from_id, to_id=to_id, good_id=good,
                                     comment_time=timezone.now, picture=pic)
        return HttpResponse('评论成功')
    else:
        return render(request, 'reply.html', {'comment':comment})
# Create your views here.
