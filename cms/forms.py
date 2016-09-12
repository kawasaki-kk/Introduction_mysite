from django.forms import ModelForm
from cms.models import Daily, Comment, Task
from django import forms
from django.forms import models
from django.forms import formsets
from django.contrib.admin.widgets import AdminDateWidget


class DailyForm(ModelForm):
    u"""Dailyモデル編集用フォーム
        Dailyモデルを編集するためのフォームです
        編集可能な項目
            title:          タイトル
            create_date:    投稿日
            report_y:       やったこと
            report_w:       わかったこと
            report_t:       つぎにやること
        タイトルと作成日について
            現在の"【日報】0830チーム開発演習デザイン作成"というようなタイトルを例にとります
                タイトル：「チーム開発演習デザイン作成」
                投稿日日：0830
            という風に対応します
            また、これは日報管理アプリであるので、「日報」であることは自明であるとします
        投稿日について
            投稿日(create_date)はカレンダーウィジェットから選択することができます
            文字列で入力する場合は"YYYY-MM-DD"という形式です
    """
    class Meta:
        model = Daily
        fields = ('title', 'create_date', 'report_y', 'report_w', 'report_t', )
        widgets = {
            'create_date': AdminDateWidget(attrs={'placeholder': 'YYYY-MM-DD'}),
            'title': forms.TextInput(attrs={
                'class': 'daily_title_form',
                'placeholder': '日報のタイトル', }),
            'report_y': forms.Textarea(attrs={
                'class': 'report_y_form',
                'placeholder': 'タスクの完了状態についてコメントしましょう'}),
            'report_w': forms.Textarea(attrs={
                'class': 'report_w_form',
                'placeholder': '一日の作業を通してわかったことやできたことを書いてください'}),
            'report_t': forms.Textarea(attrs={
                'class': 'report_t_form',
                'placeholder': '明日のタスクで気を付けることがあったらコメントしましょう'}),
        }


class TaskForm(ModelForm):
    u"""Taskモデル編集用フォーム
        Taskモデルを編集するためのフォームです
        編集可能な項目
            complete_task:  タスクの完了状態
            implement_date: タスクの実施日
            name:           タスク名
            time_plan:      予定作業時間
            time_real:      実際の作業時間
        実施日はカレンダーウィジェットから選択することができます
        文字列で入力する場合は"YYYY-MM-DD"という形式です
    """
    class Meta:
        model = Task
        fields = ('complete_task', 'implement_date', 'name', 'time_plan', 'time_real', )
        widgets = {
            'implement_date': AdminDateWidget(attrs={'placeholder': 'YYYY-MM-DD'}),
            'name': forms.TextInput(attrs={'placeholder': '作業概要'}),
            'time_plan': forms.TextInput(attrs={
                'class': 'time_plan', 'type': 'number', 'placeholder': '0'}),
            'time_real': forms.TextInput(attrs={'class': 'time_real', 'type': 'number'}),
        }


class CommentForm(ModelForm):
    u"""Commentモデル編集用フォーム
        Commentモデルを編集するためのフォームです
        編集可能な項目
            comment:    コメント本文

    """
    class Meta:
        model = Comment
        fields = ('comment', )
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'comment_form'})
        }


class SearchForm(forms.Form):
    u"""キーワード検索用入力フォーム
        キーワード検索用のキーワード入力フォームです
    """
    keyword = forms.CharField(max_length=100, required=False,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'キーワード'}))

    class Meta:
        pass


class DateForm(forms.Form):
    u"""日付絞込み用入力フォーム
        日付絞込み用の日付入力フォームです
        ウィジェットを登録していますので、カレンダーから日付を選択することもできます
    """
    date = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'YYYY-MM-DD'}))


class DailySearchForm(forms.Form):
    u"""投稿状態絞り込み用入力フォーム
        日報のレコードを絞り込むためのフォームです
        日報の状態をドロップダウンリストにより、"すべて"、"公開"、"未公開"から選択することができます
    """

    cond = forms.ChoiceField(
        choices=[("0", "すべて表示"), ("1", "公開"), ("2", "未公開")])


class TaskSearchForm(forms.Form):
    u"""日付絞込み/タスク状態絞り込み用入力フォーム
        タスクのレコードを絞り込むためのフォームです
        ウィジェットを登録していますので、カレンダーから日付を選択することもできます
        また、タスクの完了状態をドロップダウンリストにより、"すべて"、"完了"、"未完了"から選択することができます
    """
    date = forms.DateField(widget=AdminDateWidget(attrs={'placeholder': 'YYYY-MM-DD'}))
    cond = forms.ChoiceField(
        choices=[("0", "すべて表示"), ("1", "完了したタスク"), ("2", "未完了のタスク")])

u"""タスク入力/編集用フォームセット
    タスクモデルのレコード複数を一括で更新/追加するためのフォームです
    タスクレコードの表示数は、表示対象となるクエリセット数(フォーム作成時に指定)と等しく、
    それとは別に新規入力用に空のフォームを一つ持ちます

    ※以下、TaskFormSet.modelの指定までが定義です
"""
TaskFormSet = formsets.formset_factory(TaskForm, extra=1, formset=models.BaseModelFormSet)
TaskFormSet.model = Task



