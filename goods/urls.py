from django.urls import path

from .views import *


urlpatterns = [
    path('<int:book_id>', BookDetailView.as_view(), name="book_detail"),
    path('type/<int:book_type_id>', BooksWithTypeView.as_view(), name="books_with_type"),
    path('create/', CreateNewBookView.as_view(), name='create_new_book'),
    path('up_shelf/<int:book_id>', UpShelfView.as_view(), name='up_shelf'),
    path('good/<int:good_id>', GoodDetailView.as_view(), name='good_detail'),
    path('comment/<int:good_id>', CommentView.as_view(), name='comment'),
]
