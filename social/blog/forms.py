from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author','title','slug','body','image')
        widgets = {
            'title': forms.TextInput(),
            'body': forms.Textarea(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')
        widgets = {
            'name': forms.TextInput(),
            'body': forms.Textarea(),
        }
class Emailshare(forms.Form):
    name = forms.CharField(max_length =25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)
class Contact(forms.Form):
    name = forms.CharField(max_length=20)
    email  = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)