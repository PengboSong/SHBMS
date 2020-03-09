from django.urls import path
from . import views


urlpatterns = [
    path('', views.site_help, name='site_help'),
    path('guide/', views.guide, name='guide'),
    path('article/<article_id>', views.article, name='article'),
    path('notice/<notice_id>', views.notice, name='notice')
]
