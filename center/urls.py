from django.urls import path
from . import views
from django.contrib.auth.models import User

urlpatterns = [

    # http://localhost:8000/center/user_id
    path('<int:user_id>', views.personal_center, name="personal_center"),
    path('personal_info/<int:user_id>', views.personal_info, name="personal_info"),
    path('update_info/<int:user_id>', views.update_info, name='update_info'),
    path('trans_info/<int:user_id>', views.trans_info, name='trans_info'),
    path('my_book/<int:user_id>', views.my_book, name='my_book'),
    path('del_good/<int:good_id>', views.del_good, name='del_good'),
    path('sell_good/<int:good_id>', views.sell_good, name='sell_good'),
    path('my_comment/<int:user_id>', views.my_comment, name='my_comment'),
    path('reply/<int:comment_id>', views.reply, name='reply'),
    ]


