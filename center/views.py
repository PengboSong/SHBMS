from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView

from . import form
from .models import MessageRecord, TransRecord, Account
from goods.models import Goods, Book


class PersonalCenterView(TemplateView):
    template_name = "center.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.is_authenticated and request.user.pk == user_id:
            my_account = get_object_or_404(Account, user=request.user)
            context['my_goods'] = Goods.objects.filter(merchant=user_id)[:3]
            context['trans_records'] = TransRecord.objects.filter(Q(seller=request.user) | Q(buyer=request.user))[:3]
            context['my_account'] = my_account
            return self.render_to_response(context)
        else:
            return redirect('/')

class PersonalInfoView(TemplateView):
    template_name = "personal_info.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.is_authenticated and request.user.pk == user_id:
            my_account = get_object_or_404(Account, user=request.user)
            context['my_account'] = my_account
            return self.render_to_response(context)
        else:
            return redirect('/')

class UpdateInfoView(TemplateView):
    template_name = "update_info.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.is_authenticated and request.user.pk == user_id:
            my_account = get_object_or_404(Account, user=request.user)
            obj = form.UpdateInfoForm()
            context['my_account'] = my_account
            context['obj'] = obj
            return self.render_to_response(context)
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.is_authenticated and request.user.pk == user_id:
            obj = form.UpdateInfoForm(request.POST)
            if obj.is_valid():
                current_user = User.objects.filter(pk=user_id)
                current_account = Account.objects.filter(user=request.user)
                current_user.update(email=obj.cleaned_data['email'])
                current_account.update(
                    phone=obj.cleaned_data['phone'],
                    school=obj.cleaned_data['school']
                )
                return redirect('personal_info', user_id=user_id)
        else:
            return redirect('/')

class MyBookView(TemplateView):
    template_name = "my_book.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        context['my_goods'] = Goods.objects.filter(merchant=user_id)
        return context

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.is_authenticated and request.user.pk == user_id:
            context['my_goods'] = Goods.objects.filter(merchant=user_id)
            return self.render_to_response(context)
        else:
            return redirect('/')

class TransactionRecordView(TemplateView):
    template_name = "trans_record.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.is_authenticated and request.user.pk == user_id:
            context['sell_records'] = TransRecord.objects.filter(seller=request.user)
            context['buy_record'] = TransRecord.objects.filter(buyer=request.user)
            return self.render_to_response(context)
        else:
            return redirect('/')

class MyCommentView(TemplateView):
    template_name = "my_comment.html"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = context['user_id']
        if request.user.is_authenticated and request.user.pk == user_id:
            context['my_comments'] = MessageRecord.objects.filter(to_id=context['user_id'])
            return self.render_to_response(context)
        else:
            return redirect('/')

def del_good(request, good_id):
    if get_object_or_404(Account, user=request.user).status == 1:
        Goods.objects.filter(pk=good_id)[0].delete()
        return redirect('personal_center', request.user.id)
    else:
        return redirect('/')

class SellGoodView(TemplateView):
    template_name = "sell_good.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        good_id = context['good_id']
        target_good = Goods.objects.filter(id=good_id)[0]
        comments = MessageRecord.objects.filter(good_id=good_id)
        context['target_good'] = target_good
        context['buyers'] = [comment.from_id for comment in comments]
        return context

    def get(self, request, *args, **kwargs):
        if get_object_or_404(Account, user=request.user).status != 1:
            return redirect('/')

        context = self.get_context_data(**kwargs)
        context['user_id'] = request.user.pk
        target_good = context['target_good']
        if target_good.status != 1:
            messages.warning(request, '书籍未上架，不能卖出')
            return redirect('my_book', user_id=request.user.pk)
        else:
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):        
        if get_object_or_404(Account, user=request.user).status != 1:
            return redirect('/')
        
        context = self.get_context_data(**kwargs)
        context['user_id'] = request.user.pk
        buyer_id = request.POST.get('buyer')
        good_id = context['good_id']
        target_good = context['target_good']
        if buyer_id:
            # 添加交易记录
            TransRecord.objects.create(
                seller=request.user,
                goods=target_good.book,
                buyer=User.objects.filter(pk=int(buyer_id))[0],
                order_time=timezone.now(),
                price=target_good.price
            )
            # 更新销量
            current_volume = Book.objects.get(id=target_good.book.pk).sale_volume + 1
            Book.objects.filter(id=target_good.book.pk).update(sale_volume=current_volume)
            # 更新信用分
            current_credit = Account.objects.get(user=request.user).credit + 5
            Account.objects.filter(user=request.user).update(credit=current_credit)
            # 更改书籍状态
            Goods.objects.filter(id=good_id).update(status=3)

            messages.info(request, "书籍卖出成功")
        
        return redirect('my_book', user_id=request.user.pk)


class ReplyView(TemplateView):
    template_name = "reply.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_id = context['comment_id']
        comment = get_object_or_404(MessageRecord, pk=comment_id)
        context['comment'] = comment
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user_id'] = request.user.pk
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user_id'] = request.user.pk
        comment = context['comment']
        view = request.POST.get('reply')
        pic = request.POST.get('pic')
        MessageRecord.objects.create(
            content=view,
            from_id=request.user,
            to_id=comment.from_id,
            good_id=comment.good_id,
            comment_time=timezone.now,
            picture=pic
        )

        messages.success(request, "您已成功回复")
        return redirect('my_comment', user_id=request.user.pk)
