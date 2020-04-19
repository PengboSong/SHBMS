from django.urls import path
from .views import *


urlpatterns = [
    path('', SiteNoticesView.as_view(), name='site_help'),
    path('guide/', GuideView.as_view(), name='guide'),
    path('article/<article_id>', ArticleView.as_view(), name='article'),
    path('notice/<notice_id>', NoticeView.as_view(), name='notice')
]
