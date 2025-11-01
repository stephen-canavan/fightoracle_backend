from typing import Type, TypeVar
from django.db import models
from rest_framework.exceptions import ValidationError
from api.options import WeightClass

T = TypeVar("T", bound=models.TextChoices)


# Split functionality to validate ?
def validate_choices_case_insensitive(value, cls: Type[T]):
    normalised = value.upper()

    valid_values = [code for code, _ in cls.choices]
    if normalised not in valid_values:
        raise ValidationError(
            f"{value} is not a valid {cls.__name__}. Valid values are: {valid_values}"
        )
    return normalised


# Split functionality to validate ?
def filter_weight_class(queryset, value, function):
    if not value:
        return queryset
    normalised = validate_choices_case_insensitive(value, WeightClass)
    return queryset.filter(function=normalised)


def validate_boolean_parameter(value):
    value = value.strip().lower()
    if value not in ["true", "false"]:
        raise ValidationError(f"{value} is not a valid boolean parameter")
    return value
