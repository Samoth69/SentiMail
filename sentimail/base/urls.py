from django.urls import path
#from ..public_api import views
from . import views

urlpatterns = [
    path('', views.getData),
    path('upload-test/', views.postData),
    path('upload/', views.UploadFileView.as_view()),
]