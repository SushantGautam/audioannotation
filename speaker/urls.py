from django.urls import path
from . import views

app_name = 'speaker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileEditView.as_view(), name='edit_profile'),
    path('profile/verify/', views.RequestVerification.as_view(), name='verify_profile'),

    path('exam/', views.ExamSetList.as_view(), name='exam_set_list'),
    path('exam/<int:exam_id>/', views.QuestionSetList.as_view(), name='question_set_list'),
    path('exam/<int:exam_id>/exam_popup/', views.ExamPopupView.as_view(), name='exam_popup'),
    path('exam/<int:exam_id>/submit/', views.submitExam, name='exam_submit'),
]

# contract urls
urlpatterns += [
    path('contract/', views.ContractView.as_view(), name='contract'),
]
