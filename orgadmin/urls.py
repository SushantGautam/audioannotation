from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),

    path('user/<int:user_id>/block/', views.UserChangeBlock.as_view(), name='user_block'),
    path('user/<int:user_id>/unblock/', views.UserChangeBlock.as_view(), name='user_unblock'),
]

urlpatterns += [
    path('contracts/', views.ContractListView.as_view(), name='contract_list'),
    path('contracts/create/', views.ContractCreateView.as_view(), name='contract_create'),
    path('contracts/<int:pk>/edit/', views.ContractEditView.as_view(), name='contract_edit'),
]

# Speaker page URLS
urlpatterns += [
    path('records/speakers/', views.SpeakerListView.as_view(), name='speaker_list'),
    path('records/speakers/<int:pk>/', views.SpeakerDetailView.as_view(), name='speaker_detail'),
    path('speaker/<int:user_id>/verify/', views.SpeakerVerification.as_view(), name='speaker_verify'),

    path('records/contracts/', views.SpeakerContractSignList.as_view(), name='speaker_contract'),
    path('records/contracts/<int:contract_id>/verify/', views.SpeakerContractSignVerify.as_view(),
         name='speaker_contract_verify'),
]

# Worker page URLS
urlpatterns += [
    path('tasks/workers/', views.WorkerListView.as_view(), name='worker_list'),
    path('tasks/workers/<int:pk>/', views.WorkerDetailView.as_view(), name='worker_detail'),
    path('worker/<int:user_id>/verify/', views.WorkerVerification.as_view(), name='worker_verify'),

    path('tasks/contracts/', views.WorkerContractSignList.as_view(), name='worker_contract'),
    path('tasks/contracts/<int:contract_id>/verify/', views.WorkerContractSignVerify.as_view(),
         name='worker_contract_verify'),

    path('tasks/allocation/', views.WorkerTaskList.as_view(), name='worker_task_list'),
    path('tasks/<int:task_id>/verify/', views.WorkerTaskVerify.as_view(),
         name='task_verify'),
]
