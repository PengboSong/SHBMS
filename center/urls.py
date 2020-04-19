from django.urls import path
from .views import *
from django.contrib.auth.models import User

urlpatterns = [
    # http://localhost:8000/center/user_id
    path('<int:user_id>', PersonalCenterView.as_view(), name="personal_center"),
    path('personal_info/<int:user_id>', PersonalInfoView.as_view(), name="personal_info"),
    path('my_book/<int:user_id>', MyBookView.as_view(), name='my_book'),
    path('trans_info/<int:user_id>', TransactionRecordView.as_view(), name='trans_info'),
    path('my_comment/<int:user_id>', MyCommentView.as_view(), name='my_comment'),
    path('del_good/<pk>', DeleteGoodView.as_view(), name='del_good'),
    path('sell_good/<pk>', sell_good, name='sell_good'),
    path('reply/<int:comment_id>', reply, name='reply')
]
