from .base import BaseAPIException
from rest_framework import status
from rest_framework.exceptions import APIException

class NotFoundException(BaseAPIException):
    status_code = 404
    default_detail = 'Resource not found'
    error_code = "not_found"

class BadRequestException(APIException):
    status_code = 400
    default_detail = 'Bad request'
    error_code = "bad_request"

class PermissionDeniedException(APIException):
    status_code = 403
    default_detail = 'Permission denied'
    error_code = "permission_denied"
