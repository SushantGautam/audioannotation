"""XXX_PROJECT_NAME_XXX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from SoundAnnotation import settings
from WebApp import views

admin.site.site_header = 'Sound Annotation Administration'  # default: "Django Administration"
admin.site.index_title = 'Sound Annotation Administration'  # default: "Site administration"
admin.site.site_title = 'Sound Annotation Administration'  # default: "Django site admin"

urlpatterns = [
    path('', include('WebApp.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    })]

urlpatterns += [
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^accounts/profile$', views.ProfileView),
]
