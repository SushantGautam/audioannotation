from django.urls import path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('annotation/', views.AnnotationPage.as_view(), name='annotation_page'),
]
