from enum import IntEnum, Enum


class MoveType(Enum):
    stationary = 'stationary'
    normal = 'normal'
    run = 'run'


class TurnSequence(IntEnum):
    hero = 0
    movement = 1
    shooting = 2
    charge = 3
    combat = 4
    battleshock = 5


class WeaponType(IntEnum):
    missile = 0
    melee = 1
