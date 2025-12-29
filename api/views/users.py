from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import User
from api.serializers import UserSerializer
from rest_framework import viewsets
from api.permissions import IsOwner
from rest_framework.permissions import AllowAny, IsAdminUser


class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsOwner()]
        if self.action in ["destroy", "update", "partial_update"]:
            return [IsOwner() | IsAdminUser()]

        return [IsAdminUser()]

    def list(self, request):
        self.check_permissions(request)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, username=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, username=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, username=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
