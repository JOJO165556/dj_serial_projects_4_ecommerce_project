from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role =="admin"
    
class IsManager(BaseException):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role =="manager"
    
class IsSeller(BaseException):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role =="seller"
    
class IsCustomer(BaseException):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role =="customer"