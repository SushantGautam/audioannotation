from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('professor_question_list', views.QuestionListPage.as_view(), name='question_list_page'),
    path('professor_question_set', views.QuestionSetPage, name='question_set_page'),
]