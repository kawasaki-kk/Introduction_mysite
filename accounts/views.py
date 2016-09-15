from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserResisterFrom, UserEditFrom
from accounts.models import User


def register(request, user_id=None):
    comment = ''

    if request.POST:
        form = UserResisterFrom(request.POST)
        if form.is_valid():
            username = request.POST['username']
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            # screenname = request.POST['screenname']
            if request.POST['password1'] == request.POST['password2'] and request.POST['password1']:
                password = request.POST['password1']
                try:
                    new_user = User.objects._create_user(
                        username=username, first_name=first_name, last_name=last_name,
                        password=password, is_superuser=False)
                except ValueError:
                    comment = '* 無効なユーザー名です'
                    form = UserResisterFrom(request.POST)
                    return render(request, 'accounts/register.html', {'form': form, 'comment': comment})
                new_user.is_active = True
                new_user.save()
                return redirect('login')
            else:
                comment = '* パスワードが一致しません'
                form = UserResisterFrom(request.POST)
    else:
        form = UserResisterFrom()

    return render(request, 'accounts/register.html', {'form': form, 'comment': comment})


def edit(request, user_id=None):
    comment = ''
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    else:
        user = User()

    if request.POST:
        form = UserEditFrom(request.POST, {
            'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name})
        if form.is_valid():
            username = request.POST['username']
            last_name = request.POST['last_name']
            first_name = request.POST['first_name']
            # screenname = request.POST['screenname']
            try:
                new_user = User.objects._edit_user(
                    id=user_id, username=username, first_name=first_name, last_name=last_name, is_superuser=False)
            except ValueError:
                comment = '* 無効なユーザー名です'
                form = UserEditFrom(request.POST)
                return render(request, 'accounts/edit.html', {'form': form, 'comment': comment})
            new_user.is_active = True
            new_user.save()
            return redirect('user_data')
    else:
        form = UserEditFrom({
            'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name})

    return render(request, 'accounts/edit.html', {'form': form, 'comment': comment})


def user_data(request):
    user = get_object_or_404(User, pk=request.user.id)

    return render(request, 'accounts/user_data.html', {'user': user})
