from rest_framework.permissions import BasePermission

from .models import Role


class IsApproved(BasePermission):
    message = "Votre compte n'est pas encore validé."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_approved or user.is_superuser))


class IsAdminRole(BasePermission):
    message = "Réservé aux administrateurs."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.role == Role.ADMIN)
        )


class IsParent(BasePermission):
    message = "Réservé aux parents."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == Role.PARENT)


class IsNurseryManager(BasePermission):
    message = "Réservé aux responsables de crèche."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == Role.NURSERY_MANAGER)
