from .unit import Unit
from .weapon import Weapon
from .enums import WeaponType


def chainrasp_horde(*, game, x=0, y=0):
    return Unit(
        name='Chainrasp Horde',
        max_wounds=1,
        move=6,
        bravery=6,
        save=5,
        weapons=[
            Weapon(range=1, attacks=2, hit=4, wound=4, rend=0, damage=1, type=WeaponType.melee)],
        colour='blue',
        symbol='X',
        game=game,
        x=x,
        y=y,
    )
