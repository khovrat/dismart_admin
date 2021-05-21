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


@api_view(["PATCH"])
@view_status_logger
@renderer_classes([JSONRenderer])
def change_server_language(request):
    if request.method == "PATCH":
        settings.LANGUAGE_CODE = request.data['language']
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
        settings.LANGUAGE_CODE = request.data['language']
        subject = _('Thanks, ') + request.data['username']
        send_mail(
            subject,
            _('YourReviewIsVeryImportantForUs'),
            settings.EMAIL_HOST_USER,
            [request.data['email']]
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
        description = utils.create_description_payment(request.data['username'], request.data['subscription'])
        charge = stripe.Charge.create(
            amount=utils.get_amount_payment(request.data['subscription']),
            currency="usd",
            source=token,
            description=description
        )
        if charge['captured']:
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
        data = crud.read_counters(request.GET['username'])
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_companies(request):
    if request.method == "GET":
        data = serializers_wrapper.get_serialize_company(crud.read_companies_username(request.GET['username']))
        data = utils.add_completeness(data)
        data = utils.translate_market(data, request.GET['language'])
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["DELETE"])
@view_status_logger
@renderer_classes([JSONRenderer])
def delete_companies(request):
    if request.method == "DELETE":
        if crud.delete_companies_id(request.data['id']):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def detail_companies(request):
    if request.method == "GET":
        company = crud.read_companies_id(request.GET['id'])
        if company is not None:
            data = serializers_wrapper.get_serialize_company(company)
            data = utils.add_users(data, request.GET['id'])
            data.update(utils.add_all_users())
            data = utils.translate_market(data, request.GET['language'])
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_workplace(request):
    if request.method == "GET":
        data = utils.add_position(request.GET['username'])
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
        settings.LANGUAGE_CODE = request.data['language']
        subject = _('Thanks, ') + request.data['username']
        send_mail(
            subject,
            _('YourCompanyIsVeryImportantForUs'),
            settings.EMAIL_HOST_USER,
            [request.data['email']]
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