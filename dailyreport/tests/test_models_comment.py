# -*- coding: utf-8 -*-
from django.test import TestCase

from accounts.models import User
from dailyreport.models import Daily, Comment


# 6 tests
class CommentModelsTest(TestCase):
    def create_comment(self, username='', password='', title='', comment=''):
        user = User(username=username)
        user.set_password(password)
        user.save()
        daily = Daily.objects.create(user=user, title=title)
        daily.save()
        comment = Comment.objects.create(user=user, daily=daily, comment=comment)
        comment.save()

    def test_comment_is_empty(self):
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)

    def test_comment_is_not_empty(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        comment_text = 'test_comment'
        self.create_comment(username, password, title, comment_text)
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 1)

    def test_comment_saving_and_retrieving(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        comment_text = 'test_comment'
        self.create_comment(username=username, password=password,
                            title=title, comment=comment_text)
        comment = Comment.objects.all()[0]
        self.assertEqual(comment.user.username, username)
        self.assertEqual(comment.daily.title, title)
        self.assertEqual(comment.comment, comment_text)

    def test_comment_updating_and_retrieving(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        comment_text = 'test_comment'
        comment_text_update = 'test_comment_update'
        self.create_comment(username=username, password=password,
                            title=title, comment=comment_text)
        comment = Comment.objects.all()[0]
        self.assertEqual(comment.user.username, username)
        self.assertEqual(comment.daily.title, title)
        self.assertEqual(comment.comment, comment_text)
        comment.comment = comment_text_update
        comment.save()
        comment = Comment.objects.all()[0]
        self.assertEqual(comment.comment, comment_text_update)

    def test_comment_deleting(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        comment_text = 'test_comment'
        self.create_comment(username=username, password=password,
                            title=title, comment=comment_text)
        comment = Comment.objects.all()[0]
        self.assertEqual(comment.user.username, username)
        self.assertEqual(comment.daily.title, title)
        self.assertEqual(comment.comment, comment_text)
        comment.delete()
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)

    def test_comment_deleting_from_daily_deleted(self):
        username = 'test_user'
        password = 'test_password'
        title = 'test_title'
        comment_text = 'test_comment'
        self.create_comment(username=username, password=password,
                            title=title, comment=comment_text)
        comment = Comment.objects.all()[0]
        self.assertEqual(comment.user.username, username)
        self.assertEqual(comment.daily.title, title)
        self.assertEqual(comment.comment, comment_text)
        daily = Daily.objects.all()[0]
        daily.delete()
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)
