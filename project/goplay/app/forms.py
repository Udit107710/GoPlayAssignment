from django import forms
from app import views
from django.conf import settings

class PostForm(forms.ModelForm):
    class Meta:
        model = views.Post
        fields = ['file']

class LikeForm(forms.ModelForm):
    class Meta:
        model = views.Like
        fields = ['post']

class CommentForm(forms.ModelForm):
    class Meta:
        model = views.Comment
        fields = [ 'text']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = views.Reply
        fields = [ 'reply' ]
