from rest_framework.permissions import BasePermission


class UserIsOwnerOrder(BasePermission):

    def has_object_permission(self, request, view, order):
        return request.user.id == order.user.id

class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
