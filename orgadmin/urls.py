from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),

    path('user/<int:user_id>/verify/', views.UserVerification.as_view(), name='user_verify'),
    path('user/<int:user_id>/block/', views.UserChangeBlock.as_view(), name='user_block'),
    path('user/<int:user_id>/unblock/', views.UserChangeBlock.as_view(), name='user_unblock'),
]

urlpatterns += [
    path('records/speakers/', views.SpeakerListView.as_view(), name='speaker_list'),
]
