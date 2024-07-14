from rest_framework import status as statuses
from rest_framework.response import Response

"""
# ===============================================================================
# HELPERS =======================================================================
# ===============================================================================
"""


def str_to_bool(v):
    return str(v).lower() in (
        "yes",
        "true",
        "t",
        "1",
        "on",
    )


def api_response_success(message="Success!", data=None, status=statuses.HTTP_200_OK):
    return Response(
        {"success": str(message), "message": str(message), "data": data}, status=status
    )


def api_response_error(message="Error. Please try again later."):
    return Response(
        {"error": str(message), "message": str(message)},
        status=statuses.HTTP_400_BAD_REQUEST,
    )
