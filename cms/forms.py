from django.forms import ModelForm
from cms.models import Daily, Comment


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

