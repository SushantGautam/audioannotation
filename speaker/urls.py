from django.urls import path
from . import views

app_name = 'speaker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
]