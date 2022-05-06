from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orgadmin.urls')),
    path('professor/', include('professor.urls')),
    path('speaker/', include('speaker.urls')),
    path('worker/', include('worker.urls')),
]
