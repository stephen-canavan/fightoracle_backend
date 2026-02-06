from django.contrib import admin
from .models import Promotion, Event, Fight, Fighter, Prediction, User, UserStats
from api.services.events import complete_event

admin.site.register(Promotion)
admin.site.register(Fight)
admin.site.register(Fighter)
admin.site.register(User)
admin.site.register(UserStats)
admin.site.register(Prediction)


@admin.action(description="Complete selected events")
def complete_selected_events(modeladmin, request, queryset):
    for event in queryset:
        complete_event(event.id)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status")
    actions = [complete_selected_events]
