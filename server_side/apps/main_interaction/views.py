import json

import stripe
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from server_side import settings
from server_side.apps.data_interaction import crud, serializers_wrapper
from server_side.apps.main_interaction.views_base import authenticate_base
from server_side.apps.shared_logic import utils
from server_side.apps.shared_logic.loggers import view_status_logger
from server_side.apps.module_interaction.audience_forecast import (
    prediction as af_prediction,
)
from server_side.apps.module_interaction.company_forecast import (
    prediction as cf_prediction,
)
from server_side.apps.module_interaction.company_test import prediction as ct_prediction
from server_side.apps.module_interaction.market_forecast import (
    prediction as mf_prediction,
)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def change_server_language(request):
    if request.method == "PATCH":
        settings.LANGUAGE_CODE = request.data["language"]
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_amount_info(request):
    if request.method == "GET":
        data = {
            "users": crud.read_amount_users(),
            "companies": crud.read_amount_companies(),
            "articles": crud.read_amount_articles(),
            "advices": crud.read_amount_advices(),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@view_status_logger
@renderer_classes([JSONRenderer])
def sign_in(request):
    if request.method == "POST":
        return authenticate_base(request)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@view_status_logger
@renderer_classes([JSONRenderer])
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def sign_up(request):
    if request.method == "PUT":
        if crud.create_profile(request.data):
            return authenticate_base(request)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def reset_password(request):
    if request.method == "PATCH":
        crud.update_profile_password(request.data)
        return authenticate_base(request)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def save_review(request):
    if request.method == "PUT":
        crud.create_review(request.data)
        base_language = settings.LANGUAGE_CODE
        settings.LANGUAGE_CODE = request.data["language"]
        subject = _("Thanks, ") + request.data["username"]
        send_mail(
            subject,
            _("YourReviewIsVeryImportantForUs"),
            settings.EMAIL_HOST_USER,
            [request.data["email"]],
        )
        settings.LANGUAGE_CODE = base_language
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def make_payment(request):
    if request.method == "PATCH":
        token = utils.create_token(request.data)
        description = utils.create_description_payment(
            request.data["username"], request.data["subscription"]
        )
        charge = stripe.Charge.create(
            amount=utils.get_amount_payment(request.data["subscription"]),
            currency="usd",
            source=token,
            description=description,
        )
        if charge["captured"]:
            crud.update_profile_subscription(request.data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def lower_subscription(request):
    if request.method == "PATCH":
        crud.update_profile_subscription(request.data)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def change_profile(request):
    if request.method == "PATCH":
        if crud.update_profile(request.data):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def change_image(request):
    if request.method == "PATCH":
        crud.update_profile_image(request.data)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_counters(request):
    if request.method == "GET":
        data = crud.read_counters(request.GET["username"])
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_companies(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_company(
            crud.read_companies_username(request.GET["username"])
        )
        data = utils.add_completeness(data)
        data = utils.translate_market(data, request.GET["language"])
        data = utils.add_markets(data, request.GET["language"])
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
@view_status_logger
@renderer_classes([JSONRenderer])
def delete_companies(request):
    if request.method == "DELETE":
        if crud.delete_companies_id(request.data["id"]):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def detail_companies(request):
    if request.method == "GET":
        company = crud.read_companies_id(request.GET["id"])
        if company is not None:
            data = serializers_wrapper.get_serialize_company(company)
            data = utils.add_users(data, request.GET["id"])
            data.update(utils.add_all_users())
            data = utils.translate_market(data, request.GET["language"])
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_workplace(request):
    if request.method == "GET":
        data = utils.add_position(request.GET["username"])
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def change_companies(request):
    if request.method == "PATCH":
        if crud.update_company(request.data):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def change_companies_image(request):
    if request.method == "PATCH":
        crud.update_company_image(request.data)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def add_companies(request):
    if request.method == "PUT":
        crud.create_company(request.data)
        base_language = settings.LANGUAGE_CODE
        settings.LANGUAGE_CODE = request.data["language"]
        subject = _("Thanks, ") + request.data["username"]
        send_mail(
            subject,
            _("YourCompanyIsVeryImportantForUs"),
            settings.EMAIL_HOST_USER,
            [request.data["email"]],
        )
        settings.LANGUAGE_CODE = base_language
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def add_user_companies(request):
    if request.method == "PUT":
        if crud.create_workplace(request.data):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
@view_status_logger
@renderer_classes([JSONRenderer])
def delete_user_companies(request):
    if request.method == "DELETE":
        if crud.delete_workplace_username_company_position(request.data):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_reviews(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_user_review(crud.read_reviews())
        data = utils.change_date(data)
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_user_reviews(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_user_review(
            crud.read_reviews_username(request.GET["username"])
        )
        data = utils.change_date(data)
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_advices(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_advice_translation(
            crud.read_advice_translation_language(request.GET["language"])
        )
        data = utils.add_rating_advices(data, request.GET["username"])
        data = utils.add_disaster_type_translation_advice(data, request.GET["language"])
        data = {
            "advices": data,
            "disasters": utils.get_disasters_type(request.GET["language"]),
            "max_amount": utils.get_max_amount(data),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def filter_advices(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_advice_translation(
            crud.read_advice_translation_language_type(
                request.GET["language"], request.GET["type"]
            )
        )
        data = utils.add_rating_advices(data, request.GET["username"])
        data = utils.add_disaster_type_translation_advice(data, request.GET["language"])
        data = {
            "advices": data,
            "disasters": utils.get_disasters_type(request.GET["language"]),
            "max_amount": utils.get_max_amount(data),
        }
        data["advices"] = utils.filter_aid(data["advices"], request.GET)
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def rate_advices(request):
    if request.method == "PUT":
        if crud.create_advice_rating(request.data):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_articles(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_article(
            crud.read_article_language(request.GET["language"])
        )
        data = utils.add_rating_articles(data, request.GET["username"])
        data = utils.add_disaster_type_translation_article(
            data, request.GET["language"]
        )
        data = {
            "articles": data,
            "disasters": utils.get_disasters_type(request.GET["language"]),
            "max_amount": utils.get_max_amount(data),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def filter_articles(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_article(
            crud.read_article_language_type(
                request.GET["language"], request.GET["type"]
            )
        )
        data = utils.add_rating_articles(data, request.GET["username"])
        data = utils.add_disaster_type_translation_article(
            data, request.GET["language"]
        )
        data = {
            "articles": data,
            "disasters": utils.get_disasters_type(request.GET["language"]),
            "max_amount": utils.get_max_amount(data),
        }
        data["articles"] = utils.filter_aid(data["articles"], request.GET)
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def rate_articles(request):
    if request.method == "PUT":
        if crud.create_article_rating(request.data):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def create_articles(request):
    if request.method == "PUT":
        if crud.create_article(request.data):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
@view_status_logger
@renderer_classes([JSONRenderer])
def delete_articles(request):
    if request.method == "DELETE":
        if crud.delete_article_id(request.data["id"]):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def update_articles(request):
    if request.method == "PATCH":
        if crud.update_article(request.data):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_news(request):
    if request.method == "GET":
        data = {
            "news": utils.get_search_request(request.GET["language"]),
            "disasters": utils.get_disasters_type(request.GET["language"]),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def filter_news(request):
    if request.method == "GET":
        data = {
            "news": utils.filter_search_request(
                request.GET["language"], request.GET["id"]
            ),
            "disasters": utils.get_disasters_type(request.GET["language_base"]),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_disasters(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_disaster(
            crud.read_disaster_user(request.GET["username"])
        )
        data = utils.add_img(data)
        data = utils.add_disaster_type_translation_article(
            data, request.GET["language"]
        )
        data = {
            "disasters": data,
            "types": utils.get_disasters_type(request.GET["language"]),
            "companies": utils.get_companies_user(request.GET["username"]),
            "max_term": utils.get_max_term(data),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def create_disasters(request):
    if request.method == "PUT":
        if crud.create_disaster(request.data):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def update_disasters(request):
    if request.method == "PATCH":
        if crud.update_disaster(request.data):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
@view_status_logger
@renderer_classes([JSONRenderer])
def delete_disasters(request):
    if request.method == "DELETE":
        if crud.delete_disaster_id(request.data["id"]):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def filter_disasters(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_disaster(
            crud.read_disaster_user_type(request.GET["username"], request.GET["type"])
        )
        data = utils.add_img(data)
        data = utils.add_disaster_type_translation_article(
            data, request.GET["language"]
        )
        data = {
            "disasters": data,
            "types": utils.get_disasters_type(request.GET["language"]),
            "companies": utils.get_companies_user(request.GET["username"]),
            "max_term": utils.get_max_term(data),
        }
        data["disasters"] = utils.filter_disasters(data["disasters"], request.GET)
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_audience(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_audience(
            crud.read_audiences_company(request.GET["company"])
        )
        data = utils.add_img(data)
        data = utils.add_audience_type_translation(data, request.GET["language"])
        data = utils.transform_age_group(data)
        data = {
            "audiences": data,
            "types": utils.get_audience_type(request.GET["language"]),
            "max_size": utils.get_max_size(data),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
@view_status_logger
@renderer_classes([JSONRenderer])
def create_audience(request):
    if request.method == "PUT":
        if crud.create_audience(request.data):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def update_audience(request):
    if request.method == "PATCH":
        if crud.update_audience(request.data):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
@view_status_logger
@renderer_classes([JSONRenderer])
def delete_audience(request):
    if request.method == "DELETE":
        if crud.delete_audience_id(request.data["id"]):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def filter_audience(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_audience(
            crud.read_audiences_company(request.GET["company"])
        )
        data = utils.add_img(data)
        data = utils.add_audience_type_translation(data, request.GET["language"])
        data = utils.transform_age_group(data)
        data = {
            "audiences": data,
            "types": utils.get_audience_type(request.GET["language"]),
            "max_size": utils.get_max_size(data),
        }
        data["audiences"] = utils.filter_audiences(data["audiences"], request.GET)
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def forecast_audience(request):
    if request.method == "GET":
        audience = crud.read_audiences_id(request.GET["id"])
        if audience == "":
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = serializers_wrapper.get_serialize_audience(audience)
        data = utils.add_img_single(data)
        data = utils.add_audience_type_translation_single(data, request.GET["language"])
        data = utils.transform_age_group_single(data)
        data = {
            "audience": data,
            "indicators": af_prediction.make_prediction(
                data, request.GET["disaster"], request.GET["language"]
            ),
        }
        if data["indicators"] == "":
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
        crud.create_audience_forecast(
            request.GET["id"], request.GET["disaster"], data["indicators"]
        )
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def forecast_market(request):
    if request.method == "GET":
        market = crud.read_market_company_id(request.GET["id"])
        if market == "":
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = serializers_wrapper.get_serialize_market(market)
        data = utils.add_market_translation_single(data, request.GET["language"])
        data = utils.add_market_size(data)
        data = {
            "market": data,
            "data": mf_prediction.make_prediction(
                data,
                request.GET["disaster"],
                request.GET["language"],
                request.GET["method"],
            ),
        }
        if data["data"] == "":
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
        crud.create_market_forecast(
            request.GET["id"], request.GET["disaster"], data["data"]
        )
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@view_status_logger
@renderer_classes([JSONRenderer])
def test_company(request):
    if request.method == "POST":
        company = crud.read_companies_id(request.data["id"])
        if company == "":
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = serializers_wrapper.get_serialize_company(company)
        data = utils.add_amount_users(data, request.data["id"])
        data = utils.add_company_market_translation_single(
            data, request.data["language"]
        )
        data = {
            "company": data,
            "indicators": ct_prediction.make_prediction(
                data,
                request.data["disaster"],
                request.data["language"],
                request.data["info"],
            ),
        }
        if data["indicators"] == "":
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
        crud.create_company_stresstest(
            request.data["id"], request.data["disaster"], data["indicators"]
        )
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@view_status_logger
@renderer_classes([JSONRenderer])
def forecast_company(request):
    if request.method == "POST":
        company = crud.read_companies_id(request.data["id"])
        if company == "":
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = serializers_wrapper.get_serialize_company(company)
        data = utils.add_amount_users(data, request.data["id"])
        data = utils.add_company_market_translation_single(
            data, request.data["language"]
        )
        data = {
            "company": data,
            "data": cf_prediction.make_prediction(
                data,
                request.data["disaster"],
                request.data["language"],
                request.data["info"],
                json.loads(request.data["values"])
            ),
        }
        if data["data"] == "":
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
        crud.create_company_forecast(
            request.data["id"], request.data["disaster"], data["data"]
        )
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
