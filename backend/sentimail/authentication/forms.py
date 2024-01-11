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
        #fields = ('username', 'email', 'password', 'first_name', 'last_name')
        fields = ('username', 'email', 'first_name', 'last_name')
    
class AccountForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, label='Email')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, label='Email')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email does not exist")
        return email
    
class GenerateApiKeyForm(forms.Form):
    generate_api_key = forms.BooleanField(widget=forms.HiddenInput, initial=True)