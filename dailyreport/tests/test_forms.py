# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from dailyreport.forms import DailyForm, CommentForm, TaskForm, SearchForm, DateForm
from dailyreport.models import Daily, Task, Comment


# 10 tests
class DailyFormTest(TestCase):
    def test_valid(self):
        params = dict(title='test_title', create_date=timezone.now().date())
        daily = Daily()
        form = DailyForm(params, instance=daily)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        params = dict()
        daily = Daily()
        form = DailyForm(params, instance=daily)
        self.assertFalse(form.is_valid())


class TaskFormTest(TestCase):
    def test_valid(self):
        params = dict(name='test_name', time_plan=1, time_real=0, implement_date=timezone.now().date())
        task = Task()
        form = TaskForm(params, instance=task)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        params = dict()
        task = Task()
        form = TaskForm(params, instance=task)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    def test_valid(self):
        params = dict(comment='test_comment')
        comment = Comment()
        form = CommentForm(params, instance=comment)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        params = dict()
        comment = Comment()
        form = CommentForm(params, instance=comment)
        self.assertFalse(form.is_valid())


class SearchFormTest(TestCase):
    def test_valid(self):
        param = dict(keyword='test_keyword')
        form = SearchForm(param)
        self.assertTrue(form.is_valid())

    def test_valid2(self):
        u"""
            現行では、空文字での検索を許容しています
        :return:
        """
        param = dict()
        form = SearchForm(param)
        self.assertTrue(form.is_valid())


class DateFormTest(TestCase):
    def test_valid(self):
        param = dict(date=timezone.now().date())
        form = DateForm(param)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        param = dict()
        form = DateForm(param)
        self.assertFalse(form.is_valid())
