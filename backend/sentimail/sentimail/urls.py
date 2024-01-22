"""
URL configuration for sentimail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from upload import views
from django.conf import settings
from django.conf.urls.static import static
from base import views
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index, name='index'),
    path('api/', include('base.urls')),
    path('api_doc/', views.api_doc, name='api_doc'),
    #path('login/', authentication.views.login_page, name='login'),
    path('login/', authentication.views.LoginView.as_view(), name='login'),
    #path('logout/', authentication.views.logout_user, name='logout'),
    path('logout/', authentication.views.LogoutView.as_view(), name='logout'),
    #path('signup/', authentication.views.signup_page, name='signup'),
    path('signup/', authentication.views.SignupView.as_view(), name='signup'),
    path('account/', authentication.views.AccountView.as_view(), name='account'),
    path('result/<uuid:uuid>/', views.result, name='result'),
    path('historic/', views.historic, name='historic'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)