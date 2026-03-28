from rest_framework.exceptions import APIException

class BaseAPIException(APIException):
    status_code = 400
    default_detail = "Application error"
    error_code = "error"

    def __init__(self, detail=None):
        if detail:
            self.detail = detail