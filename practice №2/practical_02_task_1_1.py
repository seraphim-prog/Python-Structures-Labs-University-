"""Власний одноразовий ітератор CyclicRange."""

from operator import index


class CyclicRange:
    """Повторює діапазон із невключеною межею stop."""

    def __init__(self, start: int, stop: int, step: int = 1, repeats: int = 1):
        bounds = range(start, stop, step)  # range перевіряє параметри та step.
        self._start = bounds.start
        self._stop = bounds.stop
        self._step = bounds.step
        self._repeats = index(repeats)
        if self._repeats < 0:
            raise ValueError("Кількість повторів має бути невід'ємною.")
        self._current = self._start
        self._cycle = 0
        if self._reached_stop(self._current):
            self._cycle = self._repeats  # Порожній діапазон уже вичерпано.

    def _reached_stop(self, value: int) -> bool:
        if self._step > 0:
            return value >= self._stop
        return value <= self._stop

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self._cycle >= self._repeats:
            raise StopIteration
        value = self._current
        self._current += self._step
        if self._reached_stop(self._current):
            self._current = self._start
            self._cycle += 1
        return value


def main():
    print("CyclicRange(1, 4, repeats=3):")
    for value in CyclicRange(1, 4, repeats=3):
        print(value, end=" ")
    print()

    print("CyclicRange(0, 10, step=3, repeats=2):")
    for value in CyclicRange(0, 10, step=3, repeats=2):
        print(value, end=" ")
    print()

    print("Як список:", list(CyclicRange(5, 8, repeats=2)))
    total = sum(CyclicRange(1, 5, repeats=2))
    print("Сума CyclicRange(1, 5, repeats=2):", total)
    descending = CyclicRange(3, 1, step=-1, repeats=2)
    print("Від'ємний крок:", list(descending))
    print("Після обходу:", next(descending, "вичерпано"))
    print("Нуль повторів:", list(CyclicRange(1, 4, repeats=0)))


if __name__ == "__main__":
    main()
