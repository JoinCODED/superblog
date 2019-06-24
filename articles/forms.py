from django import forms
from django.contrib.auth.models import User
from .models import Article, Profile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

        widgets = {
            'password': forms.PasswordInput(),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', ]
