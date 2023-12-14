from django.shortcuts import render, redirect

from . import forms
from django.views.generic import View
from rest_framework.authtoken.models import Token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = "Please enter your username and password"
        return render(request, self.template_name, {'form': form, 'message': message})
    
    def post(self, request):
        form = self.form_class(request.POST)
        message = "Please enter your username and password"
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = "You are logged in"
                return redirect('index')
            else:
                message = "Invalid username or password"
        return render(request, self.template_name, {'form': form, 'message': message})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')
    
class SignupView(View):
    template_name = 'authentication/signup.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        message = "Please enter your username, email and password"
        return render(request, self.template_name, {'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = "Please enter your username, email and password"
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, self.template_name, {'form': form, 'message': message})
    
""" class PasswordResetView(View):
    template_name = 'authentication/password_reset.html'
    form_class = forms.PasswordResetForm

    def get(self, request):
        form = self.form_class()
        message = "Please enter your email"
        return render(request, self.template_name, {'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = "Please enter your email"
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, self.template_name, {'form': form, 'message': message}) """
    
class AccountView(LoginRequiredMixin, View):
    template_name = 'authentication/account.html'
    form_class = forms.AccountForm
    token_form_class = forms.GenerateApiKeyForm
    def get(self, request):
        form = self.form_class()
        message = "Please enter your email"
        token_form = self.token_form_class()
        api_key = Token.objects.filter(user=request.user).first()
        return render(request, self.template_name, {'form': form, 'token_form': token_form, 'message': message, 'api_key': api_key})

    def post(self, request):
        # Generate API key
        if 'generate_api_key' in request.POST:
            token_form = self.token_form_class(request.POST)
            if token_form.is_valid():
                user = request.user
                token, created = Token.objects.get_or_create(user=user)
                if not created:
                    token.delete()
                    token = Token.objects.create(user=user)
                print("Token: ", token)
                #return render(request, self.template_name, {'api_key': token})
                return redirect('account')
        else:
            pass

        return render(request, self.template_name, {'form': token_form})
            
        
       


""" def signup_page(request):
    form = forms.SignupForm()
    message = "Please enter your username, email and password"
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')

    return render(request, 'authentication/signup.html', {'form': form})



def login_page(request):
    form = forms.LoginForm()
    message = "Please enter your username and password"
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                #email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = "You are logged in"
                return redirect('index')
            else:
                message = "Invalid username or password"
    return render(request, 'authentication/login.html', {'form': form, 'message': message})

def logout_user(request):
    logout(request)
    return redirect(login_page) """