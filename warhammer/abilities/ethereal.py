from .abc import BaseAbility


class Ethereal(BaseAbility):
    def __init__(self):
        self.name = "Ethereal"

    def handle(self, action):
        ...
