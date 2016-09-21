# -*- coding: utf-8 -*-
from django.test import TestCase

from accounts.models import User
from dailyreport.models import Daily


# 5 tests
class DailyModelsTest(TestCase):
    def create_daily(self, username='', password='', title=''):
        user = User(username=username)
        user.set_password(password)
        user.save()
        daily = Daily.objects.create(user=user, title=title)
        daily.save()

    def test_daily_is_empty(self):
        dailys = Daily.objects.all()
        self.assertEqual(dailys.count(), 0)

    def test_daily_is_not_empty(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        self.create_daily(username, password, title)
        dailys = Daily.objects.all()
        self.assertEqual(dailys.count(), 1)

    def test_daily_saving_and_retrieving(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        self.create_daily(username=username, password=password, title=title)
        daily = Daily.objects.all()[0]
        self.assertEqual(daily.user.username, username)
        self.assertEqual(daily.title, title)

    def test_daily_updating_and_retrieving(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        title_update = 'test_title_update'
        self.create_daily(username=username, password=password, title=title)
        daily = Daily.objects.all()[0]
        self.assertEqual(daily.user.username, username)
        self.assertEqual(daily.title, title)
        daily.title = title_update
        daily.save()
        daily = Daily.objects.all()[0]
        self.assertEqual(daily.title, title_update)

    def test_daily_deleting(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        self.create_daily(username=username, password=password, title=title)
        daily = Daily.objects.all()[0]
        self.assertEqual(daily.user.username, username)
        self.assertEqual(daily.title, title)
        daily.delete()
        dailys = Daily.objects.all()
        self.assertEqual(dailys.count(), 0)

