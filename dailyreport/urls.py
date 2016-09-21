# -*- coding: utf-8 -*-
from django.conf.urls import url
from dailyreport import views

urlpatterns = [
    # 日報操作
    url(r'^dailyreport/$', views.daily_list_view, name='daily_list'),
    url(r'^dailyreport/add/$', views.daily_edit_view, name='daily_add'),
    url(r'^dailyreport/mod/(?P<daily_id>\d+)/$', views.daily_edit_view, name='daily_mod'),
    url(r'^dailyreport/del/(?P<daily_id>\d+)/$', views.delete_daily, name='daily_del'),
    url(r'^dailyreport/detail/(?P<daily_id>\d+)/$', views.daily_detail_view, name='daily_detail'),
    url(r'^dailyreport/search/$', views.search_daily_by_keyword, name='daily_search'),
    # コメント操作
    url(r'^dailyreport/comment/add/(?P<daily_id>\d+)/$', views.comment_edit_view, name='comment_add'),
    url(r'^dailyreport/comment/mod/(?P<daily_id>\d+)/(?P<comment_id>\d+)/$', views.comment_edit_view, name='comment_mod'),
    url(r'^dailyreport/comment/del/(?P<daily_id>\d+)/(?P<comment_id>\d+)/$', views.delete_comment, name='comment_del'),
    # タスク操作
    url(r'^dailyreport/task/mod/(?P<daily_id>\d+)/$', views.task_edit_in_task_page, name='task_mod'),
    url(r'^dailyreport/task/$', views.task_edit_in_daily_page, name='task_mod_daily'),
    url(r'^dailyreport/task/mod/$', views.task_edit_in_task_page, name='task_mod'),
    # ユーザーごとの日報操作
    url(r'^dailyreport/userinfo/(?P<user_id>\d+)/$', views.user_daily_view, name='user_info'),
    url(r'^dailyreport/userinfo/list/$', views.user_list_view, name='user_list'),
    url(r'^dailyreport/userinfo/search/$', views.search_user_by_keyword, name='user_search'),
]