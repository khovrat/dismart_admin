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
    path('articles/create/', views.create_articles),
    path('articles/delete/', views.delete_articles),
    path('articles/update/', views.update_articles),
    path('articles/filter/', views.filter_articles),
    path('articles/rate/', views.rate_articles),
    path('news/', views.get_news),
    path('news/filter/', views.filter_news),
    path('disasters/', views.get_disasters),
    path('disasters/create/', views.create_disasters),
    path('disasters/update/', views.update_disasters),
    path('disasters/delete/', views.delete_disasters),
    path('disasters/filter/', views.filter_disasters),
    path('audience/', views.get_audience),
    path('audience/create/', views.create_audience),
    path('audience/update/', views.update_audience),
    path('audience/delete/', views.delete_audience),
    path('audience/filter/', views.filter_audience),
    path('audience/forecast/', views.forecast_audience),
    path('market-forecast/', views.forecast_market),
    path('company-stresstest/', views.test_company),
    path('company-forecast/', views.forecast_company)
]
