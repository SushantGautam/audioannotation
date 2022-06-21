from decorator_include import decorator_include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from orgadmin.views import homepage, gitpull, migratedb, deployserver
from .permissions import authorize

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),

    path('', login_required(homepage), name='homepage'),
    path('', decorator_include([login_required, authorize(lambda u: hasattr(u, 'orgadmin'))], 'orgadmin.urls')),
    path('professor/', decorator_include([login_required, authorize(lambda u: hasattr(u, 'professor'))], 'professor.urls')),
    path('speaker/', decorator_include([login_required, authorize(lambda u: hasattr(u, 'speaker'))], 'speaker.urls')),
    path('worker/', decorator_include([login_required, authorize(lambda u: hasattr(u, 'worker'))], 'worker.urls')),
    path('summernote/', include('django_summernote.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS and settings.DEBUG:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

# URL for development phase only
if settings.DEBUG:
    urlpatterns += [
        path('gitpull/', gitpull),
        path('deployserver/', deployserver),
        path('migratedb/', migratedb)
    ]