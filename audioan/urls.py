from decorator_include import decorator_include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from orgadmin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),

    path('', include('orgadmin.urls')),
    path('professor/', include('professor.urls')),
    path('speaker/', include('speaker.urls')),
    path('worker/', include('worker.urls')),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if 'rosetta' in settings.INSTALLED_APPS and settings.DEBUG:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

# URL for development phase only
if settings.DEBUG:
    urlpatterns += [
        path('gitpull', views.gitpull),
        path('deployserver', views.deployserver),
        path('migratedb', views.migratedb)
    ]