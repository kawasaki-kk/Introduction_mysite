# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from dailyreport.models import Daily
from dailyreport.views import daily_edit_view, comment_edit_view


class DailyViewTests(TestCase):
    def test_status_in_daily_list_view(self):
        response = self.client.get(reverse('dailyreport:view_daily_list'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_status_in_daily_detail_view(self):
        response = self.client.get(reverse('dailyreport:view_daily_detail', kwargs={"daily_id": 1}), follow=True)
        self.assertEqual(response.status_code, 200)
    """
    def test_status_in_daily_add_view(self):
        response = self.client.get(reverse('dailyreport:add_daily'), follow=True)
        self.assertEqual(response.status_code, 200)
    """


class TaskViewTests(TestCase):
    """
    def test_status_in_task_edit_view(self):
        response = self.client.get(reverse('dailyreport:task_mod'), follow=True)
        self.assertEqual(response.status_code, 200)
    """


class DailyPostRequestTests(TestCase):
    def post_request(self, title):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['title'] = title
        request.POST['create_date'] = timezone.now().date()
        return request

    def create_user(self, username='', password=''):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def test_edit_can_save_a_post_request_in_daily(self):
        title = 'test_title'
        request = self.post_request(title=title)
        request.user = self.create_user(username='test_user', password='test_password')
        response = daily_edit_view(request=request, daily_id=None)
        self.assertTrue(response.url.find('dailyreport/detail/'))
    """
    def test_edit_can_not_save_a_post_request_in_daily(self):
        title = ''
        request = self.post_request(title=title)
        request.user = self.create_user(username='test_user', password='test_password')
        response = daily_edit(request=request, daily_id=None)
        self.assertIn('日報の編集', response.content.decode())
    """

class CommentPostRequestTests(TestCase):
    def post_request(self, comment):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['comment'] = comment
        return request

    def create_user(self, username='', password=''):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_daily(self, user, title=''):
        daily = Daily.objects.create(user=user, title=title)
        daily.save()
        return daily

    def test_edit_can_save_a_post_request_in_comment(self):
        comment = 'test_comment'
        request = self.post_request(comment=comment)
        request.user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(request.user, 'test_title')
        response = comment_edit_view(request=request, daily_id=daily.id)
        self.assertTrue(response.url.find('dailyreport/detail/'))

    """
    def test_edit_can_not_save_a_post_request_in_comment(self):
        comment = ''
        request = self.post_request(comment=comment)
        request.user = self.create_user(username='test_user', password='test_password')
        daily = self.create_daily(request.user, 'test_title')
        response = comment_edit(request=request, daily_id=daily.id)
        self.assertIn('コメントの編集', response.content.decode())
    """