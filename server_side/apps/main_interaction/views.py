from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from server_side.apps.data_interaction import crud
from server_side.apps.shared_logic.loggers import view_status_logger


@api_view(['GET'])
@view_status_logger
@renderer_classes([JSONRenderer])
def get_amount_info(request):
    if request.method == 'GET':
        data = {
            'users': crud.read_amount_users(),
            'companies': crud.read_amount_companies(),
            'articles': crud.read_amount_articles(),
            'advices': crud.read_amount_advices()
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
