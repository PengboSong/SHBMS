from django.urls import path
from .views import *
from django.contrib.auth.models import User

urlpatterns = [
    # http://localhost:8000/center/user_id
    path('<int:user_id>', PersonalCenterView.as_view(), name="personal_center"),
    path('personal_info/<int:user_id>', PersonalInfoView.as_view(), name="personal_info"),
    path('update_info/<int:user_id>', UpdateInfoView.as_view(), name="update_info"),
    path('my_book/<int:user_id>', MyBookView.as_view(), name='my_book'),
    path('trans_info/<int:user_id>', TransactionRecordView.as_view(), name='trans_info'),
    path('my_comment/<int:user_id>', MyCommentView.as_view(), name='my_comment'),
    path('del_good/<int:good_id>', del_good, name='del_good'),
    path('sell_good/<int:good_id>', SellGoodView.as_view(), name='sell_good'),
    path('reply/<int:comment_id>', ReplyView.as_view(), name='reply'),
]
