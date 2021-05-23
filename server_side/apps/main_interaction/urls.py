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
    path('companies/add/', views.add_companies),
    path('companies/delete/', views.delete_companies),
    path('companies/detail/', views.detail_companies),
    path('companies/detail/edit/', views.change_companies),
    path('companies/detail/image/', views.change_companies_image),
    path('companies/detail/users/add/', views.add_user_companies),
    path('companies/detail/users/delete/', views.delete_user_companies),
    path('workplace/', views.get_workplace),
    path('reviews/', views.get_reviews),
    path('reviews/personal/', views.get_user_reviews),
    path('advices/', views.get_advices),
    path('advices/filter/', views.filter_advices),
    path('advices/rate/', views.rate_advices),
    path('articles/', views.get_articles),
    path('articles/create/', views.filter_articles),
    path('articles/delete/', views.filter_articles),
    path('articles/update/', views.filter_articles),
    path('articles/filter/', views.filter_articles),
    path('articles/rate/', views.rate_articles),
]
