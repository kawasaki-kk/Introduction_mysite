# -*- coding: utf-8 -*-
"""Introduction_mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from accounts import views

urlpatterns = [
    # ユーザー関連
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^register/(?P<user_id>\d+)/$', views.edit_user, name='edit'),
    url(r'^user/$', views.view_user_data, name='user_data'),
    # 管理サイト
    url(r'^admin/', admin.site.urls),
    # 日報アプリ
    url(r'^', include('dailyreport.urls', namespace='dailyreport')),
]