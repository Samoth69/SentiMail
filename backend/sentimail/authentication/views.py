from django.shortcuts import render, redirect

from . import forms
from django.views.generic import View

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
    

def signup_page(request):
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
    return redirect(login_page)