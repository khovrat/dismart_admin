from django.contrib.auth import logout
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from server_side import settings
from server_side.apps.data_interaction import crud
from server_side.apps.main_interaction.views_base import authenticate_base
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
        crud.create_profile(request.data)
        return authenticate_base(request)
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


