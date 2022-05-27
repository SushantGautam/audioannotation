from django.urls import path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('exam/', views.ExamListView.as_view(), name='exam_list'),
    path('exam/ajax/', views.ExamListViewAjax.as_view(), name='exam_list_ajax'),
    path('myquestions/', views.QuestionSetListView.as_view(), name='question_set_list'),
]

# Annotation Tool URLs
urlpatterns += [
    path('annotation/<int:id>/', views.AnnotationPage.as_view(), name='annotation_page'),
    path('annotation/<int:id>/save/', views.SaveAnnotation.as_view(), name='save_annotation'),
]
