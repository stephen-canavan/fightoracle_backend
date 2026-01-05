import django_filters
from django.utils import timezone
from django.db.models import Q, F
from api.models import Prediction
from api.options import Method, WeightClass
from api.filters.utils import validate_choices_case_insensitive


class PredictionFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name="user__username", lookup_expr="exact")
    event = django_filters.NumberFilter(
        field_name="fight__event__id", lookup_expr="exact"
    )
    promotion = django_filters.NumberFilter(
        field_name="fight__event__promotion__id", lookup_expr="exact"
    )
    weight_class = django_filters.CharFilter(method="filter_weight_class")
    fighter_red = django_filters.NumberFilter(
        field_name="fight__fighter_red__id", lookup_expr="exact"
    )
    fighter_blue = django_filters.NumberFilter(
        field_name="fight__fighter_blue__id", lookup_expr="exact"
    )
    fighter = django_filters.NumberFilter(method="filter_fighter")
    title_fight = django_filters.BooleanFilter(field_name="fight__title_fight")
    method = django_filters.BooleanFilter(method="filter_method")

    # Time filters
    upcoming = django_filters.BooleanFilter(method="filter_upcoming")
    past = django_filters.BooleanFilter(method="filter_past")

    # Result filters
    perfect = django_filters.BooleanFilter(method="filter_perfect")
    winner_correct = django_filters.BooleanFilter(method="filter_winner_correct")
    round_correct = django_filters.BooleanFilter(method="filter_round_correct")
    method_correct = django_filters.BooleanFilter(method="filter_method_correct")

    class Meta:
        model = Prediction
        fields = {
            "user": ["exact"],
            "fight": ["exact"],
            "winner": ["exact"],
            "round": ["exact"],
            "date": ["exact"],
        }

    def filter_weight_class(self, queryset, name, value):
        if not value:
            return queryset
        normalised = validate_choices_case_insensitive(value, WeightClass)
        return queryset.filter(fight__weight_class=normalised)

    def filter_method(self, queryset, name, value):
        if not value:
            return queryset
        normalised = validate_choices_case_insensitive(value, Method)
        return queryset.filter(method=normalised)

    def filter_fighter(self, queryset, name, value):
        return queryset.filter(
            Q(fight__fighter_red__id=value) | Q(fight__fighter_blue__id=value)
        )

    def filter_upcoming(self, queryset, name, value):
        return queryset.filter(fight__event__date__gt=timezone.now())

    def filter_past(self, queryset, name, value):
        return queryset.filter(fight__event__date__lt=timezone.now())

    def filter_winner_correct(self, queryset, name, value):
        queryset = queryset.exclude(fight__winner__isnull=True)
        if value:
            return queryset.filter(winner=F("fight__winner"))
        else:
            return queryset.exclude(winner=F("fight__winner"))

    def filter_round_correct(self, queryset, name, value):
        queryset = queryset.exclude(fight__winning_round__isnull=True)
        if value:
            return queryset.filter(round=F("fight__winning_round"))
        else:
            return queryset.exclude(round=F("fight__winning_round"))

    def filter_method_correct(self, queryset, name, value):
        queryset = queryset.exclude(fight__winning_method__isnull=True)
        if value:
            return queryset.filter(method=F("fight__winning_method"))
        else:
            return queryset.exclude(method=F("fight__winning_method"))

    def filter_perfect(self, queryset, name, value):
        queryset = self.filter_winner_correct(queryset, name, value)
        queryset = self.filter_round_correct(queryset, name, value)
        queryset = self.filter_method_correct(queryset, name, value)
        return queryset
