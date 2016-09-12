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
from django.conf.urls import url, include   # ←, includeを追加
from django.contrib import admin
from accounts import views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # ユーザー認証
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}, name='logout'),
    # ユーザー登録
    url(r'^register/$', views.register, name='register'),
    # ユーザー編集
    url(r'^register/(?P<user_id>\d+)/$', views.edit, name='edit'),
    # ユーザー情報
    url(r'^user/$', views.user_data, name='user_data'),
    # 管理サイトを使用できるように登録しておく
    url(r'^admin/', admin.site.urls),
    # 実際に日報管理として動作するアプリケーションの大元のURLを登録
    url(r'^cms/', include('cms.urls', namespace='cms')),
]