from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Talk, User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

class LoginForm(forms.Form):
    username = forms.CharField(
        label="ユーザー名",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'login-form__input'})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': 'login-form__input'})
    )

class TalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ("message",)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザー名"}
        help_texts = {"username": ""}

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいメールアドレス"}
