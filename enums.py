from enum import Enum


class StateKettle(Enum):
    ON = 1
    OFF = 2


class StateKettleWater(Enum):
    COLD = 1
    HOT = 2


class Choices(Enum):
    BOIL = "1"
    FILL_WATER = "2"
    GET_WATER_COUNT = "3"
    GET_KETTLE_STATE = "4"
    GET_KETTLE_WATER_STATE = "5"
    TURN_OFF_KETTLE_BOILING = "6"
    SET_MAXIMUM_TEMP_BOILING = "7"
    EXIT = "0"
