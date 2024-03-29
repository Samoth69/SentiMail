from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register('analysis', views.EmailViewset, basename='analysis')
router.register('result', views.EmailViewsetResult, basename='result')

urlpatterns = [
    #path('analysis', views.getData),
    path('', include(router.urls)),
    #path('upload-test/', views.postData),
    path('submit/', views.UploadFileView.as_view()),
    #path('response/', views.updateResponse),
]