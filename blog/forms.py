
from django import forms
from blog.models import Comment, Reply

# コメントのフォーム作成
class CommentForm(forms.ModelForm):
    # placeholderは入力欄に薄字で表示させるコメントを設定している
    class Meta:
        model = Comment
        fields = ('name', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '名前', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'placeholder': 'コメントを入力してください', 'class': 'form-control'})
        }
        labels = {
            'name': '※必須',
            'text': '※必須'
        }


# 返信のフォーム作成
class ReplyForm(forms.ModelForm):
    # placeholderは入力欄に薄字で表示させるコメントを設定している
    class Meta:
        model = Reply
        fields = ('name', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '名前', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'placeholder': '返信を入力してください', 'class': 'form-control'})
        }
        labels = {
            'name': '※必須',
            'text': '※必須'
        }
