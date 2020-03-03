from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/book/1
    path('<int:book_id>', views.book_detail, name="book_detail"),
    path('type/<int:book_type_id>', views.books_with_type, name="books_with_type"),
    path('create/', views.create_new_book, name='create_new_book'),
    path('up_shelf/<int:book_id>', views.up_shelf, name='up_shelf'),
    path('good/<int:good_id>', views.good_detail, name='good_detail'),
    path('comment/<int:good_id>', views.comment, name='comment'),
]
