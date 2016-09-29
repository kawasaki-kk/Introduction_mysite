# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase

from dailyreport.views import \
    view_daily_list, view_daily_detail, edit_daily, search_daily_by_keyword, delete_daily
from dailyreport.views import \
    edit_task_in_task_page, edit_task_in_daily_page, view_user_of_daily, delete_comment, edit_comment


# 14 tests
class UrlResolveTestsDaily(TestCase):
    def test_url_resolves_to_daily_list(self):
        found = resolve('/dailyreport/')
        self.assertEqual(found.func, view_daily_list)

    def test_url_resolves_to_daily_add(self):
        found = resolve('/dailyreport/add/')
        self.assertEqual(found.func, edit_daily)

    def test_url_resolves_to_daily_mod(self):
        found = resolve('/dailyreport/edit/1/')
        self.assertEqual(found.func, edit_daily)

    def test_url_resolves_to_daily_del(self):
        found = resolve('/dailyreport/delete/1/')
        self.assertEqual(found.func, delete_daily)

    def test_url_resolves_to_daily_detail(self):
        found = resolve('/dailyreport/detail/1/')
        self.assertEqual(found.func, view_daily_detail)

    def test_url_resolves_to_daily_keyword_search(self):
        found = resolve('/dailyreport/search/')
        self.assertEqual(found.func, search_daily_by_keyword)


class UrlResolveTestsComment(TestCase):
    def test_url_resolves_to_comment_add(self):
        found = resolve('/dailyreport/comment/add/1/')
        self.assertEqual(found.func, edit_comment)

    def test_url_resolves_to_comment_mod(self):
        found = resolve('/dailyreport/comment/edit/1/1/')
        self.assertEqual(found.func, edit_comment)

    def test_url_resolves_to_comment_del(self):
        found = resolve('/dailyreport/comment/del/1/1/')
        self.assertEqual(found.func, delete_comment)


class UrlResolveTestsTask(TestCase):
    def test_url_resolves_to_task_list(self):
        found = resolve('/dailyreport/task/')
        self.assertEqual(found.func, edit_task_in_daily_page)

    def test_url_resolves_to_task_add(self):
        found = resolve('/dailyreport/task/edit/')
        self.assertEqual(found.func, edit_task_in_task_page)


class UrlResolveTestsOthers(TestCase):
    def test_url_resolves_to_user_info(self):
        found = resolve('/dailyreport/user/1/')
        self.assertEqual(found.func, view_user_of_daily)
