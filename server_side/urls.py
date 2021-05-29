"""server_side URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

from server_side import settings
from server_side.apps.shared_logic.views import download_logs, watch_logs

urlpatterns = [url(r'^i18n/', include('django.conf.urls.i18n')),]

urlpatterns += i18n_patterns(
    path('admin/', include('smuggler.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    prefix_default_language=True
)
urlpatterns += [
    path('admin/logs/download/', download_logs, name='download_logs'),
    path('admin/logs/watch/', watch_logs, name='watch_logs'),
    path('api/', include('server_side.apps.main_interaction.urls')),
    path('bot/', include('server_side.apps.module_interaction.urls')),
    path('django-rq/', include('django_rq.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
