from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('upload-test/', views.postData),
    path('upload/', views.UploadFileView.as_view()),
]