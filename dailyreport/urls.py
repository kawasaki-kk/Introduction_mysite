# -*- coding: utf-8 -*-
from django.conf.urls import url
from dailyreport import views

urlpatterns = [
    # 日報操作
    url(r'^dailyreport/$', views.daily_list, name='daily_list'),
    url(r'^dailyreport/add/$', views.daily_edit, name='daily_add'),
    url(r'^dailyreport/mod/(?P<daily_id>\d+)/$', views.daily_edit, name='daily_mod'),
    url(r'^dailyreport/del/(?P<daily_id>\d+)/$', views.daily_del, name='daily_del'),
    url(r'^dailyreport/detail/(?P<daily_id>\d+)/$', views.daily_detail, name='daily_detail'),
    url(r'^dailyreport/search/$', views.daily_search, name='daily_search'),
    # コメント操作
    url(r'^dailyreport/comment/add/(?P<daily_id>\d+)/$', views.comment_edit, name='comment_add'),
    url(r'^dailyreport/comment/mod/(?P<daily_id>\d+)/(?P<comment_id>\d+)/$', views.comment_edit, name='comment_mod'),
    url(r'^dailyreport/comment/del/(?P<daily_id>\d+)/(?P<comment_id>\d+)/$', views.comment_del, name='comment_del'),
    # タスク操作
    url(r'^dailyreport/task/mod/(?P<daily_id>\d+)/$', views.task_edit, name='task_mod'),
    url(r'^dailyreport/task/$', views.task_edit_daily, name='task_mod_daily'),
    url(r'^dailyreport/task/mod/$', views.task_edit, name='task_mod'),
    # ユーザーごとの日報操作
    url(r'^dailyreport/userinfo/(?P<user_id>\d+)/$', views.user_info, name='user_info'),
    url(r'^dailyreport/userinfo/list/$', views.user_list, name='user_list'),
    url(r'^dailyreport/userinfo/search/$', views.user_search, name='user_search'),
]