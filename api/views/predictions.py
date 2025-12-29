from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Prediction, User
from api.serializers import PredictionSerializer
from api.filters.prediction import PredictionFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from api.permissions import PredictionIsMakeable, IsOwner


class PredictionViewSet(viewsets.ViewSet):
    filterset_class = PredictionFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated(), PredictionIsMakeable()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwner(), PredictionIsMakeable()]
        return [IsAdminUser()]

    def get_queryset(self, **kwargs):
        query_set = Prediction.objects.all()

        username = self.kwargs.get("user_pk")

        if username:
            user = get_object_or_404(User, username=username)
            query_set = query_set.filter(user=user)

        return query_set

    def list(self, request, **kwargs):
        predictions = self.get_queryset(**kwargs)
        filterset = self.filterset_class(
            self.request.query_params, queryset=predictions
        )
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        predictions = filterset.qs
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        prediction = get_object_or_404(Prediction, id=pk)
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        prediction = get_object_or_404(Prediction, id=pk)
        prediction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
