from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


def spkt_response(data):
    return Response({
        'success': True,
        'result': data
    }, status=HTTP_200_OK)
