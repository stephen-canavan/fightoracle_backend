import django_filters
from django.db.models import Q
from api.models import Fight


class FightFilter(django_filters.FilterSet):
    fighter = django_filters.NumberFilter(method="filter_fighter")

    class Meta:
        model = Fight
        fields = {
            "event": ["exact"],
            "promotion": ["exact"],
            "fighter_red": ["exact"],
            "fighter_blue": ["exact"],
            "winner": ["exact"],
            "method": ["exact"],
            "round": ["exact"],
            "date": ["exact"],
        }

    def filter_fighter(self, queryset, name, value):
        return queryset.filter(Q(fighter_red__id=value) | Q(fighter_blue__id=value))
