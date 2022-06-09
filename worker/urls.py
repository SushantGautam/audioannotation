from django.urls import path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', views.ProfileEditView.as_view(), name='edit_profile'),
    path('profile/verify/', views.RequestVerification.as_view(), name='verify_profile'),
]

# contract urls
urlpatterns += [
    path('contract/', views.ContractView.as_view(), name='contract'),
]

# Worker Tasks URLS
urlpatterns += [
    path('exam/', views.ExamListView.as_view(), name='exam_list'),
    path('exam/ajax/', views.ExamListViewAjax.as_view(), name='exam_list_ajax'),

    path('task/create/', views.WorkerTaskCreate.as_view(), name='task_create'),

    path('task/', views.WorkerTaskListView.as_view(), name='task_list'),
    path('task/me/', views.MyTaskListView.as_view(), name='my_task_list'),

]
# Annotation Tool URLs
urlpatterns += [
    path('task/<int:workertask_id>/', views.AnnotationPage.as_view(), name='annotation_page'),
    path('annotation/<int:task_id>/save/<int:speakersubmission_id>/', views.SaveAnnotation.as_view(), name='save_annotation'),
    path('annotation/<int:task_id>/submit/<int:speakersubmission_id>/', views.WorkerTaskSubmit.as_view(), name='submit_annotation'),
]
