"""
============================================================================================ #
API RESPONSE =============================================================================== #
============================================================================================ #
"""
#
# Response type to standardize response structure and conversions
#


class ApiResponse:
    def __init__(self, status=None, message=None, results=None, **kwargs):
        self.status = status
        self.message = message
        self.results = results
        self.extras = kwargs

    def dict(self):
        res = {
            "status": self.status,
            "message": self.message,
            "results": self.results,
        }
        for key, value in self.extras.items():
            res[key] = value
        return res
