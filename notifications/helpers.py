from rest_framework import status
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


def api_response_success(message="Success!."):
    return Response({"success": message}, status=status.HTTP_200_OK)


def api_response_error(message="Error. Please try again later."):
    return Response({"error": str(message)}, status=status.HTTP_400_BAD_REQUEST)
