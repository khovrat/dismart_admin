from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from server_side.apps.data_interaction import crud
from server_side.apps.data_interaction import serializers_wrapper
from server_side.apps.shared_logic.loggers import view_status_logger


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
        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )
        if user:
            if user.is_active:
                login(request, user)
                return Response(
                    serializers_wrapper.get_serialize_profile(user.profile),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    serializers_wrapper.get_serialize_profile(user.profile),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@view_status_logger
@renderer_classes([JSONRenderer])
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@view_status_logger
@renderer_classes([JSONRenderer])
def sign_up(request):
    if request.method == "POST":
        profile = crud.create_profile(request.data)
        user = authenticate(
            username=profile.user.username, password=request.data["password"]
        )
        if user:
            if user.is_active:
                login(request, user)
                return Response(
                    serializers_wrapper.get_serialize_profile(user.profile),
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    serializers_wrapper.get_serialize_profile(user.profile),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
