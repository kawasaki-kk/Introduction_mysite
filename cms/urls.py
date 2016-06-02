from django.conf.urls import url
from cms import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 一覧
    url(r'^dailyreport/$', views.daily_list, name='daily_list'),
    # 日報操作
    url(r'^dailyreport/add/$', views.daily_edit, name='daily_add'),  # 登録
    url(r'^dailyreport/mod/(?P<daily_id>\d+)/$', views.daily_edit, name='daily_mod'),  # 修正
    url(r'^dailyreport/del/(?P<daily_id>\d+)/$', views.daily_del, name='daily_del'),   # 削除
    # コメント操作
    url(r'^dailyreport/comment/add/(?P<daily_id>\d+)/$', views.comment_edit, name='comment_add'),  # 登録
    url(r'^dailyreport/comment/mod/(?P<daily_id>\d+)/(?P<comment_id>\d+)/$', views.comment_edit, name='comment_mod'),  # 修正
    # 詳細
    url(r'^dailyreport/detail/(?P<pk>\d+)/$', views.daily_detail.as_view(), name='daily_detail'),
    # 検索
    url(r'^dailyreport/search/$', views.daily_search, name='daily_search'),
]