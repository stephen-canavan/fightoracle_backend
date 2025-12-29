from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.SimpleRouter()
# Users
router.register(r"users", views.UserViewSet, basename="user")
users = routers.NestedSimpleRouter(router, r"users", lookup="user")
users.register(r"predictions", views.PredictionViewSet, basename="user-predictions")

# Predictions
router.register(r"predictions", views.PredictionViewSet, basename="prediction")

# Promotions
router.register(r"promotions", views.PromotionViewSet, basename="promotion")
promotions = routers.NestedSimpleRouter(router, r"promotions", lookup="promotion")
promotions.register(r"events", views.EventViewSet, basename="promotion-events")

# Events
router.register(r"events", views.EventViewSet, basename="event")
events = routers.NestedSimpleRouter(router, r"events", lookup="event")
events.register(r"fights", views.FightViewSet, basename="event-fights")
events.register(r"fighters", views.FighterViewSet, basename="event-fighters")

# Fights
router.register(r"fights", views.FightViewSet, basename="fight")
fights = routers.NestedSimpleRouter(router, r"fights", lookup="fight")
fights.register(r"fighters", views.FighterViewSet, basename="fight-fighters")

# Fighters
router.register(r"fighters", views.FighterViewSet, basename="fighter")
fighters = routers.NestedSimpleRouter(router, r"fighters", lookup="fighter")
fighters.register(r"fights", views.FightViewSet, basename="fighter-fights")

# Tokens
# router.register(r"token", views.TokenObtainPairView, basename="token_obtain_parir")
# router.register(r"token/refresh", views.TokenRefreshView, basename="token_refresh")

urlpatterns = [
    path(r"token/", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(r"token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path(r"", include(router.urls)),
    path(r"", include(promotions.urls)),
    path(r"", include(events.urls)),
    path(r"", include(fights.urls)),
    path(r"", include(users.urls)),
    path(r"", include(fighters.urls)),
]
