from rest_framework import permissions
class UserHasViewRights(permissions.BasePermission):
    def has_permission(self, request, view):
        serializer = view.get_serializer()
        applabel = serializer.Meta.model._meta.label_lower
        strarray = applabel.split(".")
        user = request.user
        if user.has_perm(strarray[0] + ".view_" + strarray[1]) and not view.action in view.restrictedActions:
            return True
        return False


class UserHasChangeRights(permissions.BasePermission):
    def has_permission(self, request, view):
        serializer = view.get_serializer()
        applabel = serializer.Meta.model._meta.label_lower
        strarray = applabel.split(".")
        user = request.user
        if user.has_perm(strarray[0] + ".change_" + strarray[1]) and not view.action in view.restrictedActions:
            return True
        return False


class UserHasAddRights(permissions.BasePermission):
    def has_permission(self, request, view):
        serializer = view.get_serializer()
        applabel = serializer.Meta.model._meta.label_lower
        strarray = applabel.split(".")
        user = request.user
        if user.has_perm(strarray[0] + ".add_" + strarray[1]) and not view.action in view.restrictedActions:
            return True
        return False


class UserHasDeleteRights(permissions.BasePermission):
    def has_permission(self, request, view):
        serializer = view.get_serializer()
        applabel = serializer.Meta.model._meta.label_lower
        strarray = applabel.split(".")
        user = request.user
        if user.has_perm(strarray[0] + ".delete_" + strarray[1]):
            return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
