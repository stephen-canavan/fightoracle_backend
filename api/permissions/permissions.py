from datetime import datetime
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj == request.user


class IsOwner(BasePermission):
    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class PredictionIsMakeable(BasePermission):
    message = "You cannot make a prediction once the event start date has passed"

    def has_object_permission(self, request, view, obj):
        current_time = datetime.now()

        return current_time < obj.fight.event.date
