"""перації з двовимірними векторами через магічні методи."""

from math import hypot


class Vector2D:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"ектор ({self.x:g}; {self.y:g})"

    def __repr__(self) -> str:
        return f"Vector2D({self.x!r}, {self.y!r})"

    def __add__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        if isinstance(scalar, bool) or not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __len__(self) -> int:
        return 2

    def __abs__(self) -> float:
        return hypot(self.x, self.y)


def demo() -> None:
    a = Vector2D(3, 4)
    b = Vector2D(1, -2)
    print(f"str(a) = {str(a)}")
    print(f"repr(a) = {repr(a)}. ругий вектор: {repr(b)}")
    print("a + b =", a + b)
    print("a - b =", a - b)
    print("a * 2 =", a * 2)
    print("2 * a =", 2 * a)
    print("a == Vector2D(3, 4):", a == Vector2D(3, 4))
    print("a == b:", a == b)
    print("len(a) =", len(a))
    print("abs(a) =", abs(a))
    print("a * 1 створює новий об'єкт:", a * 1 is not a)
