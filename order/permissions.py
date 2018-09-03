from rest_framework.permissions import BasePermission


class UserIsOwnerOrder(BasePermission):

    def has_object_permission(self, request, view, order):
        return request.user.id == order.user.id
