from django.shortcuts import render
from accounts.forms import UserChangeForm, UserForm
from accounts.models import UserManager, User
from django import forms

# Create your views here.


def register(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            # screenname = request.POST['screenname']
            password = request.POST['password']
            new_user = User.objects._create_user(username=username, password=password, is_superuser=False)
            new_user.is_active = True
            new_user.save()
            return render(request, 'accounts/login.html')
    else:
        form = UserForm()

    return render(request, 'accounts/register.html', {'form': form})
