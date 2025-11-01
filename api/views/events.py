from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Event
from api.serializers import EventSerializer
from rest_framework.permissions import AllowAny


class EventViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self, pk=None, **kwargs):
        promotion_id = self.kwargs.get("promotion_pk")
        query_set = Event.objects.all()

        if promotion_id:
            query_set = query_set.filter(promotion_id=promotion_id)

        return query_set

    def list(self, request, **kwargs):
        events = self.get_queryset(**kwargs)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
