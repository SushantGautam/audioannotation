from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('professor_question_list', views.QuestionListPage.as_view(), name='question_list_page'),
    path('professor_question_create_ajax', views.QuestionsCreateView.as_view(), name='question_create_ajax'),
    path('professor_question/<int:pk>/update', views.QuestionsUpdateView.as_view(), name='question_update'),
    path('professor_question/<int:pk>/detail', views.QuestionDetailView.as_view(), name='question_detail'),
    path('professor_question/<int:pk>/delete', views.QuestionDeleteView, name='question_delete'),
    path('professor_question/delete_multiple_question', views.MultipleQuestionDeleteView, name='delete_multiple_question'),
    path('professor_question_set', views.QuestionSetPage, name='question_set_page'),
]