from django.conf.urls import url
from cms import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 書籍
    url(r'^book/$', views.book_list, name='book_list'),   # 一覧
    url(r'^book/add/$', views.book_edit, name='book_add'),  # 登録
    url(r'^book/mod/(?P<book_id>\d+)/$', views.book_edit, name='book_mod'),  # 修正
    url(r'^book/del/(?P<book_id>\d+)/$', views.book_del, name='book_del'),   # 削除
    url(r'^impression/(?P<book_id>\d+)/$', views.ImpressionList.as_view(), name='impression_list'),  # 一覧
    url(r'^impression/add/(?P<book_id>\d+)/$', views.impression_edit, name='impression_add'),  # 登録
    url(r'^impression/mod/(?P<book_id>\d+)/(?P<impression_id>\d+)/$', views.impression_edit, name='impression_mod'),
    # 修正
    url(r'^impression/del/(?P<book_id>\d+)/(?P<impression_id>\d+)/$', views.impression_del, name='impression_del'),
    # 削除

    # 一覧
    url(r'^dailyreport/$', views.daily_list, name='daily_list'),
    # 日報操作
    url(r'^dailyreport/add/$', views.daily_edit, name='daily_add'),  # 登録
    url(r'^dailyreport/mod/(?P<daily_id>\d+)/$', views.daily_edit, name='daily_mod'),  # 修正
    url(r'^dailyreport/del/(?P<daily_id>\d+)/$', views.daily_del, name='daily_del'),   # 削除
    # コメント操作
    url(r'^dailyreport/comment/add/(?P<daily_id>\d+)/$', views.comment_edit, name='comment_add'),  # 登録
    url(r'^dailyreport/comment/mod/(?P<daily_id>\d+)/(?P<impression_id>\d+)/$', views.comment_edit, name='comment_mod'),  # 修正
    # 詳細
    # 編集
    # 削除
]