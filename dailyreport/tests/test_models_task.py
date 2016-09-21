# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from dailyreport.models import Task


# 3 tests
class TaskModelsTest(TestCase):
    def create_task(self, username='', password='', name='', time_plan=1, implement_date=timezone.now().date()):
        user = User(username=username)
        user.set_password(password)
        user.save()
        task = Task.objects.create(user=user, name=name, time_plan=time_plan, implement_date=implement_date)
        task.save()

    def test_task_is_empty(self):
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 0)

    def test_task_is_not_empty(self):
        username = 'test_user'
        password = 'test_password'
        name = 'test_name'
        time_plan = 1
        implement_date = timezone.now().date()
        self.create_task(username, password, name, time_plan, implement_date)
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 1)

    def test_comment_saving_and_retrieving(self):
        username = 'test_user'
        password = 'test_password'
        name = 'test_name'
        time_plan = 1
        implement_date = timezone.now().date()
        self.create_task(username, password, name, time_plan, implement_date)
        task = Task.objects.all()[0]
        self.assertEqual(task.user.username, username)
        self.assertEqual(task.name, name)
        self.assertEqual(task.time_plan, time_plan)
        self.assertEqual(task.time_real, 0)
        self.assertEqual(task.implement_date, implement_date)

