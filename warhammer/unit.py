from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums import MoveType
from .utils import roll
from .weapon import Weapon


@dataclass
class Unit:
    name: str
    move: str
    save: int
    max_wounds: int
    bravery: int
    weapons: list[Weapon]
    colour: str
    symbol: str
    game: Any
    wounds: int = 0
    x: int = 0
    y: int = 0

    def __str__(self):
        return f'[{self.colour}]{self.symbol}[/{self.colour}]'

    def make_move(self, *, move_type: MoveType) -> int:
        # currently, this will only move on the horizontal axis.
        # however, there are plans to create an algorithm to determine the positions the unit can be placed in
        # and allow the user to select the position.
        self.game.write(
            f'[bold red]Chosen [yellow]{move_type.value}[/yellow].[/]')
        if move_type == MoveType.normal:
            self.game.write(
                f'[bold red]Moving [yellow]{self.move}[/yellow] inch(es).[/]')
            self.x += self.move
        elif move_type == MoveType.run:
            value = self.move + self.game.roll()
            self.game.write(
                f'[bold red]Moving [yellow]{value}[/yellow] inch(es).[/]')
            self.x += value
        else:
            self.game.write(f'[bold red]Did not move.[/]')
            # must mean that move_type == MoveType.stationary, can be safely ignored.

    def shoot(self, weapon: Weapon) -> int:
        # hit roll
        total_hit = 0
        for _ in range(weapon.attacks):
            value = self.game.roll()
            if value >= weapon.hit:
                total_hit += value

        # wound roll

        total_damage = 0
        for _ in range(total_hit):
            value = self.game.roll()
            if value >= weapon.wound:
                total_damage += weapon.damage

        # inflict damage

        return total_damage

    def charge(self, enemy_unit: Unit):
        self.game.write('[bold red]Roll 2D6.[/]')
        value = self.game.roll() + self.game.roll()
        self.game.write(f'[bold red]Charge roll is {value}.[/]')

        print(enemy_unit.x, enemy_unit.y, self.x, self.y)
        # exit()

        if enemy_unit.y == enemy_unit.y and enemy_unit.x - self.x <= 3:
            self.game.write(
                f'[bold red]You are within 3 inches of a {enemy_unit.name}.[/]')
            self.game.write(f'[bold red]Charge failed.[/]')
            return

        self.x += value
