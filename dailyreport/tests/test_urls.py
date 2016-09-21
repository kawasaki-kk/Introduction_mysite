# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from dailyreport.views import daily_list_view, daily_detail_view, daily_edit_view, search_daily_by_keyword, delete_daily
from dailyreport.views import edit_task_in_task_page, user_daily_view, delete_comment, comment_edit_view


# 14 tests
class UrlResolveTestsDaily(TestCase):
    def test_url_resolves_to_daily_list(self):
        found = resolve('/dailyreport/')
        self.assertEqual(found.func, daily_list_view)

    def test_url_resolves_to_daily_add(self):
        found = resolve('/dailyreport/add/')
        self.assertEqual(found.func, daily_edit_view)

    def test_url_resolves_to_daily_mod(self):
        found = resolve('/dailyreport/mod/1/')
        self.assertEqual(found.func, daily_edit_view)

    def test_url_resolves_to_daily_del(self):
        found = resolve('/dailyreport/del/1/')
        self.assertEqual(found.func, delete_daily)

    def test_url_resolves_to_daily_detail(self):
        found = resolve('/dailyreport/detail/1/')
        self.assertEqual(found.func, daily_detail_view)

    def test_url_resolves_to_daily_keyword_search(self):
        found = resolve('/dailyreport/search/')
        self.assertEqual(found.func, search_daily_by_keyword)


class UrlResolveTestsComment(TestCase):
    def test_url_resolves_to_comment_add(self):
        found = resolve('/dailyreport/comment/add/1/')
        self.assertEqual(found.func, comment_edit_view)

    def test_url_resolves_to_comment_mod(self):
        found = resolve('/dailyreport/comment/mod/1/1/')
        self.assertEqual(found.func, comment_edit_view)

    def test_url_resolves_to_comment_del(self):
        found = resolve('/dailyreport/comment/del/1/1/')
        self.assertEqual(found.func, delete_comment)


class UrlResolveTestsTask(TestCase):
    def test_url_resolves_to_task_mod(self):
        found = resolve('/dailyreport/task/mod/1/')
        self.assertEqual(found.func, edit_task_in_task_page)

    def test_url_resolves_to_task_add(self):
        found = resolve('/dailyreport/task/mod/')
        self.assertEqual(found.func, edit_task_in_task_page)


class UrlResolveTestsOthers(TestCase):
    def test_url_resolves_to_user_info(self):
        found = resolve('/dailyreport/userinfo/1/')
        self.assertEqual(found.func, user_daily_view)
