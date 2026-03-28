from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        roles = getattr(view, 'allowed_roles', None) or self.__class__.allowed_roles
        return request.user.role in roles


class IsAdmin(HasRole):
    allowed_roles = ['admin']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in self.allowed_roles


class IsManager(HasRole):
    allowed_roles = ['manager']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in self.allowed_roles


class IsSeller(HasRole):
    allowed_roles = ['seller']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in self.allowed_roles


class IsCustomer(HasRole):
    allowed_roles = ['customer']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in self.allowed_roles