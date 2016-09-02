from django.core.urlresolvers import resolve
from django.test import TestCase
from cms.views import daily_list, daily_detail, daily_edit, daily_search, daily_del, daily_date_search
from cms.views import task_edit, task_date_search, user_info, comment_del, comment_edit


# 14 tests
class UrlResolveTestsDaily(TestCase):
    def test_url_resolves_to_daily_list(self):
        found = resolve('/cms/dailyreport/')
        self.assertEqual(found.func, daily_list)

    def test_url_resolves_to_daily_add(self):
        found = resolve('/cms/dailyreport/add/')
        self.assertEqual(found.func, daily_edit)

    def test_url_resolves_to_daily_mod(self):
        found = resolve('/cms/dailyreport/mod/1/')
        self.assertEqual(found.func, daily_edit)

    def test_url_resolves_to_daily_del(self):
        found = resolve('/cms/dailyreport/del/1/')
        self.assertEqual(found.func, daily_del)

    def test_url_resolves_to_daily_detail(self):
        found = resolve('/cms/dailyreport/detail/1/')
        self.assertEqual(found.func, daily_detail)

    def test_url_resolves_to_daily_date_search(self):
        found = resolve('/cms/dailyreport/daily/date/')
        self.assertEqual(found.func, daily_date_search)

    def test_url_resolves_to_daily_keyword_search(self):
        found = resolve('/cms/dailyreport/search/')
        self.assertEqual(found.func, daily_search)


class UrlResolveTestsComment(TestCase):
    def test_url_resolves_to_comment_add(self):
        found = resolve('/cms/dailyreport/comment/add/1/')
        self.assertEqual(found.func, comment_edit)

    def test_url_resolves_to_comment_mod(self):
        found = resolve('/cms/dailyreport/comment/mod/1/1/')
        self.assertEqual(found.func, comment_edit)

    def test_url_resolves_to_comment_del(self):
        found = resolve('/cms/dailyreport/comment/del/1/1/')
        self.assertEqual(found.func, comment_del)


class UrlResolveTestsTask(TestCase):
    def test_url_resolves_to_task_mod(self):
        found = resolve('/cms/dailyreport/task/mod/1/')
        self.assertEqual(found.func, task_edit)

    def test_url_resolves_to_task_add(self):
        found = resolve('/cms/dailyreport/task/mod/')
        self.assertEqual(found.func, task_edit)

    def test_url_resolves_to_task_date_search(self):
        found = resolve('/cms/dailyreport/task/mod/date/')
        self.assertEqual(found.func, task_date_search)


class UrlResolveTestsOthers(TestCase):
    def test_url_resolves_to_user_info(self):
        found = resolve('/cms/dailyreport/userinfo/1/')
        self.assertEqual(found.func, user_info)
