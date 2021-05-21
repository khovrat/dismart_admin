from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from server_side.apps.main_interaction import views

urlpatterns = [
    path('change-server-language/', views.change_server_language),
    path('amount-info/', views.get_amount_info),
    path('sign-in/', views.sign_in),
    path('sign-out/', views.sign_out),
    path('sign-up/', views.sign_up),
    path('reset-password/', views.reset_password),
    path('save-review/', views.save_review),
    path('make-payment/', views.make_payment),
    path('lower-subscription/', views.lower_subscription),
    path('change-profile/', views.change_profile),
    path('change-image/', views.change_image),
    path('counters/', views.get_counters),
    path('companies/', views.get_companies),
    path('companies/delete/', views.delete_companies),
    path('companies/detail/', views.detail_companies),
]
