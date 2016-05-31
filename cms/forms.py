from django.forms import ModelForm
from cms.models import Book, Impression, User, Daily, Comment


class BookForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Book
        fields = ('name', 'publisher', 'page', )


class ImpressionForm(ModelForm):
    """感想のフォーム"""
    class Meta:
        model = Impression
        fields = ('comment', )


class DailyForm(ModelForm):
    """日報のフォーム"""
    class Meta:
        model = Daily
        fields = ('report', )


class UserForm(ModelForm):
    """日報のフォーム"""
    class Meta:
        model = User
        fields = ('id', 'name', 'password',)


class CommentForm(ModelForm):
    """日報のフォーム"""
    class Meta:
        model = Comment
        fields = ('comment', )

