from django.contrib import admin
from .models import (
    Promotion,
    Event,
    Fight,
    Fighter,
    Prediction,
    Odds,
    User
)

admin.site.register(Promotion)
admin.site.register(Event)
admin.site.register(Fight)
admin.site.register(Fighter)
admin.site.register(User)
admin.site.register(Prediction)
admin.site.register(Odds)
