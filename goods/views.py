from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView

from . import form
from .models import Book, Goods, BookType
from homepage.views import get_sub_categories
from center.models import MessageRecord, TransRecord, Account


class BookListView(TemplateView):
    template_name = "book_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(book_status=1)
        context['sub_categories'] = get_sub_categories()
        return context


class BookDetailView(TemplateView):
    template_name = "book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = context['book_id']
        book = get_object_or_404(Book, pk=book_id)
        context['book'] = book
        context['goods'] = Goods.objects.filter(Q(book=book) & Q(status=1))
        context['sub_categories'] = get_sub_categories()
        return context


class BooksWithTypeView(TemplateView):
    template_name = "books_with_type.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_type_id = context['book_type_id']
        book_type = get_object_or_404(BookType, pk=book_type_id)
        context['book_type'] = book_type
        context['books'] = Book.objects.filter(book_type=book_type)
        context['sub_categories'] = get_sub_categories()
        return context


class CreateNewBookView(TemplateView):
    template_name = "create_new_book.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_categories'] = get_sub_categories()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if get_object_or_404(Account, user=request.user).status == 1:
            obj = form.BookModelForm()
            context['obj'] = obj
            return self.render_to_response(context)
        else:
            return HttpResponse('您无权限进行此操作')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if get_object_or_404(Account, user=request.user).status != 1:
            return HttpResponse('您无权限进行此操作')

        obj = form.BookModelForm(request.POST)
        file_obj = request.FILES.get('pic')
        if obj.is_valid():
            post = obj.save(commit=False)
            post.picture = file_obj
            post.status = 2
            post.save()
            return HttpResponse("数据提交成功，正在等待审核，审核通过后即可上架")
        else:
            context['obj'] = obj
            return self.render_to_response(context)


class UpShelfView(TemplateView):
    template_name = "up_shelf.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = context['book_id']
        context['book'] = Book.objects.filter(pk=book_id)[0]
        context['sub_categories'] = get_sub_categories()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if get_object_or_404(Account, user=request.user).status == 1:
            obj = form.GoodsModelForm()
            context['obj'] = obj
            return self.render_to_response(context)
        else:
            return HttpResponse('您无权限进行此操作')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        book = context['book']
        if get_object_or_404(Account, user=request.user).status != 1:
            return HttpResponse('您无权限进行此操作')

        obj = form.GoodsModelForm(request.POST)
        file_obj_1 = request.FILES.get('pic1')
        file_obj_2 = request.FILES.get('pic2')
        if obj.is_valid():
            post = obj.save(commit=False)
            post.status = 1
            post.book = book
            post.merchant = request.user
            post.picture_1 = file_obj_1
            post.picture_2 = file_obj_2
            post.save()
            return HttpResponse("数据提交成功！")
        else:
            context['obj'] = obj
            return self.render_to_response(context)


class GoodDetailView(TemplateView):
    template_name = "good_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        good_id = context['good_id']
        sell_book = TransRecord.objects.filter(seller=self.request.user)
        credit_point = get_object_or_404(Account, user=self.request.user).credit
        context['good'] = Goods.objects.filter(pk=good_id)[0]
        context['sell_count'] = len(sell_book)
        context['credit_point'] = credit_point
        context['sub_categories'] = get_sub_categories()
        return context


class CommentView(TemplateView):
    template_name = "comment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        good_id = context['good_id']
        context['good'] = get_object_or_404(Goods, pk=good_id)
        context['sub_categories'] = get_sub_categories()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if get_object_or_404(Account, user=request.user).status == 1:
            return self.render_to_response(context)
        else:
            return HttpResponse('您无权限进行此操作')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if get_object_or_404(Account, user=request.user).status != 1:
            return HttpResponse('您无权限进行此操作')

        good = context['good']
        comment = request.POST.get('comment')
        MessageRecord.objects.create(
            content=comment,
            from_id=request.user,
            to_id=good.merchant,
            good_id=good,
            comment_time=timezone.now
        )
        return HttpResponse("评论成功")
