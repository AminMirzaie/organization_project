from rest_framework import permissions
from . models import Roll
from . import serializers
class UpdateOwnProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not(user.is_authenticated) and (request.method == "POST"):
            return True
        elif user.is_authenticated:
            if user.roll == Roll.ADMIN:
                if request.method == "POST":
                    return False
                else:
                    return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.roll == Roll.MANAGER:
                if (request.method == "GET") and (obj.roll == Roll.ORG_WORKER) and (obj.organization == request.user.organization):
                    return True
                if (request.method == "DELETE") and (obj.roll == Roll.ORG_WORKER) and (obj.organization == request.user.organization):
                    return True
            elif request.user.roll == Roll.ADMIN:
                return True
            elif request.user.roll == Roll.ORG_WORKER:
                if request.method in permissions.SAFE_METHODS or request.method == "PUT" or request.method == "PATCH":
                    return True
                else:
                    return False
            elif request.user.roll == Roll.WORKER:
                if request.method in permissions.SAFE_METHODS or request.method == "PUT" or request.method == "PATCH":
                    return True
                else:
                    return False
            return obj.id == request.user.id
        else:
            """ User is not authenticated """
            if request.method == "POST":
                return True
            else:
                return False

class WorkerToManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.roll == Roll.ADMIN:
                if request.method in permissions.SAFE_METHODS:
                    return True
                return False
            elif user.roll == Roll.MANAGER:
                return False
            elif user.roll == Roll.WORKER:
                return True
            elif user.roll == Roll.ORG_WORKER:
                return False
        return False
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.roll == Roll.ADMIN:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
        elif user.roll == Roll.WORKER:
            return obj.from_user.id == user.id
        else:
            return False


class WorkerToOrgeWorkerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.roll == Roll.ADMIN:
                return False
            elif user.roll == Roll.MANAGER:
                if request.method in permissions.SAFE_METHODS:
                    return True
                else:
                    return False
            elif user.roll == Roll.WORKER:
                return True
            elif user.roll == Roll.ORG_WORKER:
                return False
        return False
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.roll == Roll.MANAGER:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
        elif user.roll == Roll.WORKER:
            return obj.from_user.id == user.id
        else:
            return False



class OrgWorkerToManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.roll == Roll.ADMIN:
                return False
            elif user.roll == Roll.MANAGER:
                if request.method in permissions.SAFE_METHODS:
                    return True
                else:
                    return False
            elif user.roll == Roll.WORKER:
                return False
            elif user.roll == Roll.ORG_WORKER:
                return True
        return False
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.roll == Roll.MANAGER:
            if request.method in permissions.SAFE_METHODS:
                return True
            return False
        elif user.roll == Roll.ORG_WORKER:
            return obj.from_user.id == user.id
        else:
            return False


class AcceptPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.roll == Roll.ADMIN:
                if request.method in permissions.SAFE_METHODS:
                    return True
                else:
                    return False
            elif user.roll == Roll.MANAGER:
                if request.method in permissions.SAFE_METHODS:
                    return True
                else:
                    return False
            elif user.roll == Roll.WORKER:
                return False
            elif user.roll == Roll.ORG_WORKER:
                return False
        return False


class DutyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not(request.user.is_authenticated):
            return False
        if request.user.roll == Roll.WORKER:
            return False
        if request.user.roll == Roll.ADMIN and request.method == "POST":
            return False
        else:
            return True
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.roll == Roll.MANAGER:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return obj.owner.id == user.id
        elif user.roll == Roll.ADMIN:
            return True
        if user.roll == Roll.ORG_WORKER:
            return obj.owner.id == user.id
        return False


class EditOrganizationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.roll == Roll.ADMIN:
            return True
        else:
            return False
