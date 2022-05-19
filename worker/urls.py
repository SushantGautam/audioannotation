from django.urls import path
from . import views

app_name = 'worker'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('annotation/<int:id>/', views.AnnotationPage.as_view(), name='annotation_page'),
    path('annotation/<int:id>/save/', views.SaveAnnotation.as_view(), name='save_annotation'),
]
