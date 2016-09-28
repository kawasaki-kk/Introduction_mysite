# -*- coding: utf-8 -*-
from django.conf.urls import url

from dailyreport import views

urlpatterns = [
    # 日報操作
    url(r'^dailyreport/$', views.view_daily_list, name='view_daily_list'),
    url(r'^dailyreport/add/$', views.edit_daily, name='add_daily'),
    url(r'^dailyreport/mod/(?P<daily_id>\d+)/$', views.edit_daily, name='edit_daily'),
    url(r'^dailyreport/del/(?P<daily_id>\d+)/$', views.delete_daily, name='delete_daily'),
    url(r'^dailyreport/detail/(?P<daily_id>\d+)/$', views.view_daily_detail, name='view_daily_detail'),
    url(r'^dailyreport/search/$', views.search_daily_by_keyword, name='search_daily'),
    # コメント操作
    url(r'^dailyreport/comment/add/(?P<daily_id>\d+)/$', views.edit_comment, name='add_comment'),
    url(r'^dailyreport/comment/mod/(?P<daily_id>\d+)/(?P<comment_id>\d+)/$', views.edit_comment, name='edit_comment'),
    url(r'^dailyreport/comment/del/(?P<daily_id>\d+)/(?P<comment_id>\d+)/$', views.delete_comment, name='delete_comment'),
    # タスク操作
    url(r'^dailyreport/task/$', views.edit_task_in_daily_page, name='edit_task_in_daily'),
    url(r'^dailyreport/task/mod/$', views.edit_task_in_task_page, name='edit_task'),
    # ユーザーごとの日報操作
    url(r'^dailyreport/user/(?P<user_id>\d+)/$', views.view_user_of_daily, name='view_user_daily'),
    url(r'^dailyreport/user/list/$', views.view_user_list, name='view_all_user_list'),
    url(r'^dailyreport/user/search/$', views.search_user_by_keyword, name='search_user'),
]