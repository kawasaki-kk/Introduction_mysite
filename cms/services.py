from django.shortcuts import get_object_or_404
from cms.models import Daily, Comment, Task
from cms.forms import DailyForm, CommentForm, SearchForm
from . import forms
import datetime


def init_form():
    dict(search_form=SearchForm())
    return dict


def create_task_form(user_id, daily_id=None):
    if daily_id:
        form = forms.TaskFormSet(queryset=Task.objects.filter(
            user=user_id,
            daily=daily_id
        ).order_by('name'))
    else:
        form = forms.TaskFormSet(queryset=Task.objects.filter(
            user=user_id,
            implement_date__lte=datetime.date.today()
        ).order_by('name'))
    return form


def get_task(user_id, daily):
    task_y = Task.objects.filter(user=user_id, implement_date__lte=daily.create_date).order_by('name')
    task_t = Task.objects.filter(user=user_id, daily__id=daily.id).order_by('name')
    return dict(task_y=task_y, task_t=task_t)


def get_daily_list(user_id=None, release=None):
    if user_id & release:   # ほかの人の投稿一覧
        dailys = Daily.objects.filter(user=user_id, release=release).order_by('-create_date')
    elif user_id:           # 自分の投稿一覧
        dailys = Daily.objects.filter(user=user_id).order_by('-create_date')
    elif release:           # 公開されている全投稿一覧＝普通に見れるトップページの内容
        dailys = Daily.objects.filter(release=release).order_by('-create_date')
    else:                   # 全投稿の取得
        dailys = Daily.objects.all()
    return dict(dailys=dailys)


def get_daily(user_id, daily_id=None):
    if daily_id:
        daily = get_object_or_404(Daily, pk=daily_id)
    else:
        daily = Daily(user=user_id)
    return dict(daily=daily)


def edit_comment(request, daily, comment_id=None):
    if comment_id:
        comment = get_object_or_404(Comment, pk=comment_id)
    else:
        comment = Comment(user=request.user)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.daily = daily
            comment.save()
    else:
        comment_form = CommentForm(instance=comment)
    return dict(comment_form=comment_form)


def edit_daily(request, daily):
    if request.method == 'POST':
        report_form = DailyForm(request.POST, instance=daily)
        if report_form.is_valid():
            daily = report_form.save(commit=False)
            if 'release' in request.POST:
                daily.release = True
            daily.save()  # 日報の登録
    else:  # GET の時
        report_form = DailyForm(instance=daily)
    return dict(report_form=report_form)


def edit_task(request, daily=None):
    if daily:
        pass
    else:
        daily = Daily.objects.filter(user=request.user).order_by('-create_date')[0]

    if request.method == 'POST':
        formset = forms.TaskFormSet(request.POST or None)
        if formset.is_valid():
            if 'edit' in request.POST:
                formset.save()
            elif 'add' in request.POST:
                task = Task(daily=daily, user=request.user,
                            name=formset.forms[-1].cleaned_data['name'],
                            time_plan=formset.forms[-1].cleaned_data['time_plan'],
                            time_real=formset.forms[-1].cleaned_data['time_real'],
                            implement_date=formset.forms[-1].cleaned_data['implement_date'], )
                task.save()
    else:
        pass
    return True

