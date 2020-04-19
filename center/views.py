from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import MessageRecord, TransRecord, Account
from goods.models import Goods, Book
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView


class PersonalCenterView(TemplateView):
    template_name = "center.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.id == user_id:
            context['my_goods'] = Goods.objects.filter(merchant=user_id)[:3]
            context['trans_records'] = TransRecord.objects.filter(Q(seller=request.user) | Q(buyer=request.user))[:3]
            return self.render_to_response(context)
        else:
            return redirect('/')

class PersonalInfoView(TemplateView):
    template_name = "personal_info.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.id == user_id:
            my_account = get_object_or_404(Account, user=request.user)
            context['my_account'] = my_account
            return self.render_to_response(context)
        else:
            return redirect('/')

class MyBookView(TemplateView):
    template_name = "my_book.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.id == user_id:
            context['my_goods'] = Goods.objects.filter(merchant=user_id)
            return self.render_to_response(context)
        else:
            return redirect('/')

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        context['my_goods'] = Goods.objects.filter(merchant=user_id)
        return context

    def del_good(self, request, pk):
        good_object = Goods.objects.filter(pk=pk)[0]
        # good_object.delete()
        messages.success(self.request, "商品删除成功")
        context = self.get_context_data()
        return self.render_to_response(context)

class TransactionRecordView(TemplateView):
    template_name = "trans_record.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.id == user_id:
            context['sell_records'] = TransRecord.objects.filter(seller=request.user)
            context['buy_record'] = TransRecord.objects.filter(buyer=request.user)
            return self.render_to_response(context)
        else:
            return redirect('/')

class MyCommentView(TemplateView):
    template_name = "trans_record.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if request.user.id == context['user_id']:
            context['my_comments'] = MessageRecord.objects.filter(to_id=context['user_id'])
            return self.render_to_response(context)
        else:
            return redirect('/')

class DeleteGoodView(DeleteView):
    model = Goods
    success_url = reverse_lazy('my_book')

def sell_good(request, good_id):
    target_good = Goods.objects.filter(id=good_id)[0]
    comments = MessageRecord.objects.filter(good_id=good_id)
    buyers = [comment.from_id for comment in comments]
    context = {
        'target_good': target_good,
        'buyers': buyers,
    }
    if request.method == "POST":
        buyer_id = request.POST.get('buyer')
        TransRecord.objects.create(seller=request.user, goods=target_good.book, buyer=User.objects.filter(pk=int(buyer_id))[0], order_time=timezone.now(), price=target_good.price)
        Goods.objects.filter(id=good_id).update(status=3)
        messages.success(request, "商品卖出成功")
        return render(request, 'info.html')
    elif target_good.status != 1:
        messages.warning(request, '商品未上架，不能卖出')
        return render(request, 'my_book.html', context)
    else:
        return HttpResponse('您无权限进行该操作')

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
        messages.success(request, '评论成功')
        return render(request, 'info.html')
    else:
        return render(request, 'reply.html', {'comment':comment})
