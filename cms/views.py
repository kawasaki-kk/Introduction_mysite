from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from cms.models import Daily, Comment
from cms.forms import DailyForm, CommentForm, SearchForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.db.models import Q


# 日報の一覧
def daily_list(request):
    """日報の一覧"""
#    return HttpResponse('日報の一覧')
    dailys = Daily.objects.all().order_by('date')
    return render(request,
                  'cms/daily_list.html',     # 使用するテンプレート
                  {'dailys': dailys})         # テンプレートに渡すデータ


class daily_detail(DetailView):
    model = Daily
    template_name = 'cms/daily_detail.html'


# 日報の編集
def daily_edit(request, daily_id=None):
    """日報の編集"""
    if daily_id:   # id が指定されている (修正時)
        daily = get_object_or_404(Daily, pk=daily_id)
        if daily.user != request.user:  # 投稿者とログインユーザが異なる場合
            return redirect('login')
    else:         # id が指定されていない (追加時)
        daily = Daily(user=request.user)

    if request.method == 'POST':
        form = DailyForm(request.POST, instance=daily)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            daily = form.save(commit=False)
            daily.save()
            return redirect('cms:daily_list')
    else:    # GET の時
        form = DailyForm(instance=daily)  # book インスタンスからフォームを作成

    return render(request, 'cms/daily_edit.html', dict(form=form, daily_id=daily_id))


# 日報の削除
def daily_del(request, daily_id):
    """日報の削除"""
    daily = get_object_or_404(Daily, pk=daily_id)
    daily.delete()
    return redirect('cms:daily_list')


# 日報の検索
def daily_search(request):
    form = SearchForm(request.POST)
    dailys = Daily.objects.all().filter(Q(title__contains=form.cleaned_data['keyword']) |
                                        Q(report__contains=form.cleaned_data['keyword']))
    return render(request,
                  'cms/daily_list.html',  # 使用するテンプレート
                  {'dailys': dailys})  # テンプレートに渡すデータ


# コメントの編集
def comment_edit(request, daily_id, comment_id=None):
    """感想の編集"""
    daily = get_object_or_404(Daily, pk=daily_id)  # 親の書籍を読む
    if comment_id:   # impression_id が指定されている (修正時)
        comment = get_object_or_404(Comment, pk=comment_id)
    else:               # impression_id が指定されていない (追加時)
        comment = Comment(user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            comment = form.save(commit=False)
            comment.daily = daily  # この感想の、親の書籍をセット
            comment.save()
            return redirect('cms:daily_list')
    else:    # GET の時
        form = CommentForm(instance=comment)  # impression インスタンスからフォームを作成

    return render(request,
                  'cms/comment_edit.html',
                  dict(form=form, daily_id=daily_id, comment_id=comment_id))