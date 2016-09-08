from django.shortcuts import render, redirect
from accounts.forms import UserChangeForm, UserForm, UserResisterFrom
from accounts.models import UserManager, User
from django import forms

# Create your views here.


def register(request):
    comment = ''
    if request.POST:
        form = UserResisterFrom(request.POST)
        if form.is_valid():
            username = request.POST['username']
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            # screenname = request.POST['screenname']
            if request.POST['password1'] == request.POST['password2']:
                password = request.POST['password1']
                new_user = User.objects._create_user(
                    username=username, first_name=first_name, last_name=last_name, password=password, is_superuser=False)
                new_user.is_active = True
                new_user.save()
                return redirect('login')
            else:
                comment = 'パスワードが一致しません'
                form = UserResisterFrom(request.POST)
    else:
        form = UserResisterFrom()

    return render(request, 'accounts/register.html', {'form': form, 'comment': comment})
