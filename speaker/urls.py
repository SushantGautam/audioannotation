from django.urls import path
from . import views

app_name = 'speaker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('save_audio/', views.save_audio, name='save_audio'),
    path('question_set_list/', views.QuestionSetList.as_view(), name='question_set_list'),
]