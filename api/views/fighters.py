from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Fighter
from api.serializers import FighterSerializer
from rest_framework.permissions import AllowAny


class FighterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk")
        fight_id = self.kwargs.get("fight_pk")
        query_set = Fighter.objects.all()

        if event_id:
            # fights = Fight.objects.get(event_id=event_id)
            pass

        if fight_id:
            pass

        return query_set

    def list(self, request, **kwargs):
        fighters = self.get_queryset()
        serializer = FighterSerializer(fighters, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        fighter = get_object_or_404(Fighter, id=pk)
        serializer = FighterSerializer(fighter)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        fighter = get_object_or_404(Fighter, id=pk)
        fighter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
