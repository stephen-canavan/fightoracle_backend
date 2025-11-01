from .users import UserSerializer
from .promotions import PromotionSerializer
from .events import EventSerializer
from .fighters import FighterSerializer
from .fights import FightSerializer
from .predictions import PredictionSerializer

__all__ = [
    UserSerializer,
    PromotionSerializer,
    EventSerializer,
    FighterSerializer,
    FightSerializer,
    PredictionSerializer,
]
