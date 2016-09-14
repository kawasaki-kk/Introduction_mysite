from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.utils import timezone
from accounts.models import User
from cms.services import *


class DailyModelServicesTests(TestCase):
    def post_request(self, title):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['title'] = title
        request.POST['create_date'] = timezone.now().date()
        return request

    def get_request(self, date=None, cond=None):
        request = HttpRequest()
        request.method = 'GET'
        if date:
            request.GET['date'] = date
        if cond:
            request.GET['cond'] = cond
        return request

    def create_user(self, username='', password=''):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_daily(self, user, title='', release=False):
        daily = Daily.objects.create(user=user, title=title, release=release)
        daily.save()
        return daily

    def test_get_all_daily_list_all_daily(self):
        title = 'test_title'
        user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(user=user, title=title)
        dailys = get_all_daily_list(self.get_request(), True)
        self.assertEqual(dailys.count(), 0)
        dailys = get_all_daily_list(self.get_request(), False)
        self.assertEqual(dailys.count(), 1)
        self.assertEqual(title, dailys[0].title)

    def test_get_all_daily_list_all_daily_date(self):
        title = 'test_title'
        user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(user=user, title=title)
        dailys = get_all_daily_list(self.get_request(date=timezone.now().date()), False)
        self.assertEqual(dailys.count(), 1)
        self.assertEqual(title, dailys[0].title)

    def test_get_user_daily_list_all(self):
        title = 'test_title'
        user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(user=user, title=title)
        dailys = get_user_daily_list(self.get_request(), user)
        self.assertEqual(dailys.count(), 1)
        self.assertEqual(title, dailys[0].title)

    def test_get_user_daily_list_not_release(self):
        title = 'test_title'
        user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(user=user, title=title)
        dailys = get_user_daily_list(self.get_request(cond=2), user)
        self.assertEqual(dailys.count(), 1)

    def test_get_user_daily_list_release(self):
        title = 'test_title'
        user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(user=user, title=title)
        dailys = get_user_daily_list(self.get_request(cond=1), user)
        self.assertEqual(dailys.count(), 0)


class CommentModelServicesTests(TestCase):
    def post_request(self, title):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['comment'] = title
        return request

    def get_request(self, date=None, cond=None):
        request = HttpRequest()
        request.method = 'GET'
        if date:
            request.GET['date'] = date
        if cond:
            request.GET['cond'] = cond
        return request

    def create_user(self, username='', password=''):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_daily(self, user, title='', release=False):
        daily = Daily.objects.create(user=user, title=title, release=release)
        daily.save()
        return daily

    def create_comment(self, user, daily, comment=''):
        comment = Comment.objects.create(user=user, daily=daily, comment=comment)
        comment.save()
        return comment

    def test_get_comments_from_daily(self):
        title = 'test_title'
        comment_text = 'test_comment'
        user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(user=user, title=title)
        comment = self.create_comment(user, daily, comment_text)
        comments = get_comments_from_daily(daily)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comment_text, comments[0].comment)

