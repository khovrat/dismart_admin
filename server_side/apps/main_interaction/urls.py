from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from server_side.apps.main_interaction import views


urlpatterns = [
    path('amount-info/', views.get_amount_info),
]