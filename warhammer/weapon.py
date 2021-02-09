from dataclasses import dataclass
from warhammer.enums import WeaponType


@dataclass
class Weapon:
    range: int
    attacks: int
    hit: int
    wound: int
    rend: int
    damage: int
    type: WeaponType
