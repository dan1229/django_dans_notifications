import logging

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .api_response import ApiResponse

logger = logging.getLogger(__name__)

"""
============================================================================================ #
API RESPONSE HANDLER ======================================================================= #
============================================================================================ #
"""


#
# Generic response handler to help manage (primarily) API responses
#
# This is used out of the box to provide standardized response formats,
# as well as a centralized place to edit/mangle said responses.
#
# Mainly just 'wrap' Responses/data you are already returning, this class
# can help enforce structure or format such that you can have responses
# look however you choose.
#
class ApiResponseHandler:
    def __init__(
        self,
        message_error="Error. Please try again later.",
        message_success="Successfully completed request.",
        print_log=True,
    ):
        self.message_error = message_error
        self.message_success = message_success
        self.print_log = print_log

    @staticmethod
    def format_response(response, results, message, status):
        api_response = ApiResponse(message=message, status=status, results=results)
        if response:  # response passed -> simply edit
            api_response.extras = response.data
        return Response(api_response.dict(), status=status)

    def handle_logging(self, print_log, msg):
        if print_log is None:  # print_log not passed, go by default
            if self.print_log:
                logger.error(msg)
        else:  # print_log passed, go by that
            if print_log:
                logger.error(msg)

    #
    # RESPONSES
    #
    def response_success(
        self,
        message=None,
        results=None,
        response=None,
        status=HTTP_200_OK,
    ):
        """
        @[PARAM]
        message         - message to include
        results         - results to include in response
        response        - response to edit
        status          - status to use

        @[RETURN]
        Response({
                'message': <str:message>,
                'status': <int:status>,
                'results': results,
                ... - if given 'response' other keys will be included
        })
        """
        # no message = use default
        if not message or message == "":
            message = self.message_success
        message = str(message)

        return self.format_response(
            response=response, results=results, message=message, status=status
        )

    def response_error(
        self,
        error=None,
        message=None,
        results=None,
        response=None,
        print_log=None,
        status=HTTP_400_BAD_REQUEST,
    ):
        """
        @[PARAM]
        error           - error message
        results         - results to include in response
        response        - response to edit
        status          - status to use

        @[RETURN]
        Response({
                'message': <str:message>,
                'status': <int:status>,
                'results': results,
                ... - if given 'response' other keys will be included
        })
        """
        # no message - use default
        if not message or message == "":
            message = self.message_error
        message = str(message)

        # no error - use message
        if not error or error == "":
            error = message
        error = str(error)

        self.handle_logging(print_log, error)
        return self.format_response(
            response=response, results=results, message=message, status=status
        )
