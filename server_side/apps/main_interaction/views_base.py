from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response

from server_side.apps.data_interaction import serializers_wrapper
from server_side.apps.shared_logic import utils


def authenticate_base(request):
    user = authenticate(
        username=request.data["username"], password=request.data["password"]
    )
    if user:
        if user.is_active:
            login(request, user)
            data = serializers_wrapper.get_serialize_profile(user.profile)
            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
