# -*- coding: utf-8 -*-
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from accounts.forms import UserForm, UserEditFrom, UserResisterFrom
from accounts.models import User
from accounts.views import register_user, edit_user, view_user_data


class UrlResolveTestsUser(TestCase):
    def test_url_resolves_to_login(self):
        found = resolve('/login/')
        self.assertEqual(found.func, login)

    def test_url_resolves_to_logout(self):
        found = resolve('/logout/')
        self.assertEqual(found.func, logout)

    def test_url_resolves_to_register(self):
        found = resolve('/register/')
        self.assertEqual(found.func, register_user)

    def test_url_resolves_to_edit(self):
        found = resolve('/register/1/')
        self.assertEqual(found.func, edit_user)

    def test_url_resolves_to_user_data(self):
        found = resolve('/user/')
        self.assertEqual(found.func, view_user_data)


class UserModelsTest(TestCase):
    def create_user(self, username='', password=''):
        user = User(username=username)
        user.set_password(password)
        user.save()

    def test_user_is_empty(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_user_is_not_empty(self):
        username = 'test_user'
        password = 'test_password'
        self.create_user(username, password)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_user_saving_and_retrieving(self):
        username = 'test_user'
        password = 'test_password'
        self.create_user(username=username, password=password)
        user = User.objects.all()[0]
        self.assertEqual(user.username, username)
        self.assertIs(user.check_password(password), True)


class UserFormTest(TestCase):
    def test_valid(self):
        params = dict(username='test_user', password='test_password',
                      first_name='test_first', last_name='test_last')
        user = User()
        form = UserForm(params, instance=user)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        params = dict()
        user = User()
        form = UserForm(params, instance=user)
        self.assertFalse(form.is_valid())


class UserEditFormTest(TestCase):
    def test_valid(self):
        params = dict(username='test_user', first_name='test_first', last_name='test_last')
        form = UserEditFrom(params)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        params = dict()
        form = UserEditFrom(params)
        self.assertFalse(form.is_valid())


class UserResisterFromTest(TestCase):
    def test_valid(self):
        params = dict(username='test_user', first_name='test_first', last_name='test_last',
                      password1='test_password', password2='test_password')
        form = UserResisterFrom(params)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        params = dict()
        form = UserResisterFrom(params)
        self.assertFalse(form.is_valid())

    def test_invalid_of_password(self):
        params = dict(username='test_user', first_name='test_first', last_name='test_last',
                      password1='test_password', password2='test_password_mistakes')
        form = UserResisterFrom(params)
        self.assertFalse(form.is_valid())


class ViewTest(TestCase):
    def test_status_in_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_status_in_edit_view(self):
        response = self.client.get(reverse('edit', kwargs={'user_id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
