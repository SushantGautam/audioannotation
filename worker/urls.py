from django.urls import path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
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
    path('annotation/<int:id>/', views.AnnotationPage.as_view(), name='annotation_page'),
    path('annotation/<int:id>/save/', views.SaveAnnotation.as_view(), name='save_annotation'),
]
