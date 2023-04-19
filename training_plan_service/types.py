from enum import Enum


class FilterProperty(Enum):
    SEX = "sex"
    GOAL = "goal"
    LEVEL = "level"
    FREQUENCY = "frequency"
    ENVIRONMENT = "environment"


class Sex(Enum):
    MALE = "Чоловік"
    FEMALE = "Жінка"


class Goal(Enum):
    MUSCLE_GAIN = "Набір маси"
    WEIGHT_LOSS = "Схуднення"
    IMPROVE_HEALTH = "Рельєф"


class Level(Enum):
    BEGINNER = "Початківець"
    MIDDLE = "Середній"
    ADVANCED = "Просунений"


class Frequency(Enum):
    TWICE = "Двічі на тиждень"
    THRICE = "Тричі на тиждень"
    FOUR = "Чотири рази на тиждень"


class Environment(Enum):
    GYM = "Спортзал"
    HOUSE_AND_STREET = "Дім + вулиця"


FilterEnum = Sex | Goal | Environment | Level | Frequency
