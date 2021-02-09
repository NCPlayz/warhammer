from time import sleep

from pynput import keyboard
from rich import box
from rich.console import Console
from rich.table import Table

from .board import Board
from .enums import MoveType, TurnSequence, WeaponType
from .presets import chainrasp_horde
from .unit import Unit
from .utils import int_to_die, roll
from .weapon import Weapon


class Game:
    def __init__(self):
        self.started = False
        self.phase = TurnSequence.hero
        self.units: list[Unit] = [chainrasp_horde(game=self)]
        self.enemy_units: list[Unit] = [chainrasp_horde(game=self, x=76, y=15)]
        self.console = Console()
        self.current_roll = 0
        self.messages = []
        self.board = Board()

    def start(self):
        self.write(
            '[bold red]Welcome to [yellow]Warhammer: Age of Sigmar[/yellow].[/]')
        self.write('[bold red]This is a Work-In-Progress Project.[/]')
        self.units.append(chainrasp_horde(game=self))
        self.fill_enemy_units()
        self.placement()
        self.shooting()
        self.command()
        self.charge()
        sleep(5)

    def display(self):
        self.console.clear()

        # Game statuses
        table = Table(show_header=True)
        table.add_column("Roll")
        table.add_column("Units")
        table.add_column("Record Log")
        table.add_row(
            int_to_die(self.current_roll).replace("●", "[red]●[/red]"),
            "\n".join(f'[yellow]{i}[/yellow]. [bold {unit.colour}]{unit.name} ({unit.symbol})[/]' for i,
                      unit in enumerate(self.units, start=1)),
            "\n".join(self.messages[-5:])
        )
        self.console.print(table)

        # Battlefield
        table = Table(show_header=False, show_footer=False, box=box.ROUNDED)
        table.add_column(width=100)
        table.add_row(str(self.board))
        self.console.print(table)

    def write(self, content: str):
        self.messages.append(content)
        self.display()
        sleep(1)
    
    def fill_enemy_units(self):
        for unit in self.enemy_units:
            self.board.board[unit.y][unit.x] = unit

    def prompt_command(self, unit: Unit):
        self.write(f'[bold red]Moving [yellow]{unit.name}[/yellow].[/]')
        self.write(
            '[bold red]Make your move ([blue]stationary[/blue]|[blue]normal[/blue]|[blue]run[/blue]).[/]')
        validating_move = True
        while validating_move:
            move = input('\u001b[32m> ')
            # the ANSI escape code makes the input green as well.
            print('\u001b[0m', end='')
            # At the moment, rich cannot do this.
            move.lower()
            try:
                mt = MoveType(move)
            except ValueError:
                self.write(
                    '[bold italic magenta]That was not a valid move.[/]')
            else:
                old_x, old_y = unit.x, unit.y
                unit.make_move(move_type=mt)
                self.board.board[old_y][old_x] = None
                self.board.board[unit.y][unit.x] = unit
                self.display()
                validating_move = False

    def placement(self):
        self.write('[bold red]Preparing to place units.[/]')
        for unit in self.units:
            self.place_unit(unit)

    def place_unit(self, unit: Unit):
        self.write(
            f'[bold red]Place your [yellow]{unit.name}[/yellow] (Press ESC to finish).[/]')
        x, y = 0, 0
        self.board.board[y][x] = unit
        self.display()

        def on_press(key):
            try:
                # Alphanumeric character.
                key.char
            except AttributeError:
                nonlocal x, y
                self.board.board[y][x] = None

                if key == keyboard.Key.right:
                    x += 1
                    if x > 25:
                        x = 0
                elif key == keyboard.Key.left:
                    x -= 1
                    if x < 0:
                        x = 25
                elif key == keyboard.Key.up:
                    y -= 1
                    if y < 0:
                        y = 24
                elif key == keyboard.Key.down:
                    y += 1
                    if y > 24:
                        y = 0

                self.board.board[y][x] = unit
                self.display()

        def on_release(key):
            if key == keyboard.Key.esc:
                return False

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

        unit.x, unit.y = x, y

    def charge(self):
        self.write('[green]Entering Charge Phase.[/green]')
        self.phase = TurnSequence.charge

        can_charge = False
        for unit in self.units:
            for enemy_unit in self.enemy_units:
                if enemy_unit.x - unit.x <= 12 or unit.x - enemy_unit.x <= 12:
                    can_charge = True
                    unit.charge(enemy_unit)

        if not can_charge:
            self.write(
                '[bold red]No units are eligible to charge.[/]')
            self.write('[bold red]Skipping...[/]')

    def shooting(self):
        self.write('[green]Entering Shooting Phase.[/green]')
        self.phase = TurnSequence.shooting
        have_missile_weapon = False
        for unit in self.units:
            for weapon in unit.weapons:
                if weapon.type == WeaponType.missile:
                    have_missile_weapon = True
                    # currently, none of the units have a missile weapon.

        if not have_missile_weapon:
            self.write(
                '[bold red]No units are equipped with a missile weapon.[/]')
            self.write('[bold red]Skipping...[/]')

    def command(self):
        self.write('[green]Entering Command Phase.[/green]')
        self.phase = TurnSequence.movement
        for unit in self.units:
            self.prompt_command(unit)

    def roll(self):
        self.write(f'[bold red]Rolling...[/]')
        value = roll()
        self.current_roll = value
        self.display()
        self.write(f'[bold red]Rolled a [yellow]{value}[/yellow].[/]')
        self.reset_roll()
        return value

    def reset_roll(self):
        self.current_roll = 0
        self.display()
        return
