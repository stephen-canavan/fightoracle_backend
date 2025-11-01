from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Promotion
from api.serializers import PromotionSerializer
from rest_framework.permissions import AllowAny


class PromotionViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Promotion.objects.all()

    def list(self, request):
        promotions = self.get_queryset()
        serializer = PromotionSerializer(promotions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        promotion = get_object_or_404(Promotion, id=pk)
        serializer = PromotionSerializer(promotion)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        promotion = get_object_or_404(Promotion, id=pk)
        promotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
