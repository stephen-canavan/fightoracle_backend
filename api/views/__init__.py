from .users import UserViewSet
from .events import EventViewSet
from .promotions import PromotionViewSet
from .fighters import FighterViewSet
from .fights import FightViewSet
from .predictions import PredictionViewSet

__all__ = [
    UserViewSet,
    EventViewSet,
    PromotionViewSet,
    FighterViewSet,
    FightViewSet,
    PredictionViewSet,
]
