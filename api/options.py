from django.db import models


class Promotions(models.TextChoices):
    UFC = "UFC", "Ultimate Fighting Championship"
    PFL = "PFL", "Professional Fighters League"
    BELLA = "Bellator", "Bellator MMA"
    ONE = "ONE", "ONE Championship"


## Fights
class WeightClass(models.TextChoices):
    STRAWWEIGHT = "SW", "Strawweight"
    FLYWEIGHT = "FLY", "Flyweight"
    BANTAMWEIGHT = "BW", "Bantamweight"
    FEATHERWEIGHT = "FW", "Featherweight"
    LIGHTWEIGHT = "LW", "Lightweight"
    WELTERWEIGHT = "WW", "Welterweight"
    MIDDLEWEIGHT = "MW", "Middleweight"
    LIGHTHEAVYWEIGHT = "LHW", "Light Heavyweight"
    HEAVYWEIGHT = "HW", "Heavyweight"
    SUPERHEAVYWEIGHT = "SHW", "Super Heavyweight"
    CATCHWEIGHT = "CW", "Catchweight"


class FightStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class EventStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class Method(models.TextChoices):
    FINISH = "FINISH"
    KOTKO = "KO/TKO"
    DEC = "DEC"
    SPLIT = "DEC-SPLIT"
    SUB = "SUB"
    KO = "KO"
    DQ = "DQ"
    NOC = "NC"


class Bookmaker(models.TextChoices):
    BET365 = "Bet365"
    PADDYPOWER = "PaddyPower"


class PredictionStatus(models.TextChoices):
    PENDING = "PENDING"
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"
