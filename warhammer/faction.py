class Unit:
    def __init__(self, type, *, name="", length=10):
        self.name = name
        self.length = length
        self.population = [type() for _ in range(length)]

    def __repr__(self) -> str:
        return f'<Unit name={self.name!r} length={self.length!r}>'
