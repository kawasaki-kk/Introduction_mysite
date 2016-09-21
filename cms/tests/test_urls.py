# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from cms.views import daily_list, daily_detail, daily_edit, daily_search, daily_del
from cms.views import task_edit, user_info, comment_del, comment_edit


# 14 tests
class UrlResolveTestsDaily(TestCase):
    def test_url_resolves_to_daily_list(self):
        found = resolve('/dailyreport/')
        self.assertEqual(found.func, daily_list)

    def test_url_resolves_to_daily_add(self):
        found = resolve('/dailyreport/add/')
        self.assertEqual(found.func, daily_edit)

    def test_url_resolves_to_daily_mod(self):
        found = resolve('/dailyreport/mod/1/')
        self.assertEqual(found.func, daily_edit)

    def test_url_resolves_to_daily_del(self):
        found = resolve('/dailyreport/del/1/')
        self.assertEqual(found.func, daily_del)

    def test_url_resolves_to_daily_detail(self):
        found = resolve('/dailyreport/detail/1/')
        self.assertEqual(found.func, daily_detail)

    def test_url_resolves_to_daily_keyword_search(self):
        found = resolve('/dailyreport/search/')
        self.assertEqual(found.func, daily_search)


class UrlResolveTestsComment(TestCase):
    def test_url_resolves_to_comment_add(self):
        found = resolve('/dailyreport/comment/add/1/')
        self.assertEqual(found.func, comment_edit)

    def test_url_resolves_to_comment_mod(self):
        found = resolve('/dailyreport/comment/mod/1/1/')
        self.assertEqual(found.func, comment_edit)

    def test_url_resolves_to_comment_del(self):
        found = resolve('/dailyreport/comment/del/1/1/')
        self.assertEqual(found.func, comment_del)


class UrlResolveTestsTask(TestCase):
    def test_url_resolves_to_task_mod(self):
        found = resolve('/dailyreport/task/mod/1/')
        self.assertEqual(found.func, task_edit)

    def test_url_resolves_to_task_add(self):
        found = resolve('/dailyreport/task/mod/')
        self.assertEqual(found.func, task_edit)


class UrlResolveTestsOthers(TestCase):
    def test_url_resolves_to_user_info(self):
        found = resolve('/dailyreport/userinfo/1/')
        self.assertEqual(found.func, user_info)
