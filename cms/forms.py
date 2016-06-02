from django.forms import ModelForm
from cms.models import Daily, Comment
from django import forms


class DailyForm(ModelForm):
    """日報のフォーム"""
    class Meta:
        model = Daily
        fields = ('title', 'report', )


class CommentForm(ModelForm):
    """日報のフォーム"""
    class Meta:
        model = Comment
        fields = ('comment', )


# 検索用フォーム
class SearchForm(forms.Form):
    keyword = forms.CharField()
