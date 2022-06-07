from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('professor_question_list', views.QuestionListPage.as_view(), name='question_list_page'),
    path('professor_question_create_ajax', views.QuestionsCreateView.as_view(), name='question_create_ajax'),
    path('professor_question_set_create', views.QuestionSetCreateView.as_view(), name='question_set_create'),
    path('professor_question_set/<int:pk>/update', views.QuestionsSetUpdateView.as_view(), name='question_set_update'),
    path('professor_question/<int:pk>/update', views.QuestionsUpdateView.as_view(), name='question_update'),
    path('professor_question/<int:pk>/detail', views.QuestionDetailView.as_view(), name='question_detail'),
    path('professor_question/<int:pk>/delete', views.QuestionDeleteView, name='question_delete'),
    path('professor_question/<int:pk>/delete/question_set', views.QuestionSetDeleteView, name='questionset_delete'),
    path('professor_question/delete_multiple_question', views.MultipleQuestionDeleteView, name='delete_multiple_question'),
    path('professor_question/delete_multiple_question_set', views.MultipleQuestionSetDeleteView, name='delete_multiple_questionset'),
    path('professor_question_set', views.QuestionSetListView.as_view(), name='question_set_page'),
    path('category_management', views.CategoryManagementListView.as_view(), name='category_management_page'),
]