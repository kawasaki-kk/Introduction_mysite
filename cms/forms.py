from django.forms import ModelForm
from cms.models import Daily, Comment, Task
from django import forms
from django.forms import models
from django.forms import formsets
from django.contrib.admin.widgets import AdminDateWidget


class DailyForm(ModelForm):
    """日報のフォーム"""
    class Meta:
        model = Daily
        fields = ('title', 'report_y', 'report_w', 'report_t', )


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ('complete_task', 'implement_date', 'name', 'time_plan', 'time_real', )
        widgets = {'implement_date': AdminDateWidget, }


class CommentForm(ModelForm):
    """日報のフォーム"""
    class Meta:
        model = Comment
        fields = ('comment', )


# 検索用フォーム
class SearchForm(forms.Form):
    # 検索キーワード
    keyword = forms.CharField(max_length=100, required=False)

TaskFormSet = formsets.formset_factory(TaskForm, extra=1, formset=models.BaseModelFormSet)
TaskFormSet.model = Task



