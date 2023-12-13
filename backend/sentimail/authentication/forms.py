from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    #email = forms.EmailField(widget=forms.EmailInput, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
    