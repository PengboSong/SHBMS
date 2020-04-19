"""SHBMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from homepage.views import *
from goods.views import book_list
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),
    path('book/', include('goods.urls')),
    path('book/', book_list, name='book'),
    path('search/', search, name='search'),
    path('center/', include('center.urls')),
    path('help/', include('help.urls')),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('update_password/', update_password, name='update_password'),
    path('check_email/', check_email, name='check_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
