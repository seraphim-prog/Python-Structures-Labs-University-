"""Інкапсуляція на прикладі температурного датчика."""


class TemperatureSensor:
    MIN_CELSIUS = -50
    MAX_CELSIUS = 150

    def __init__(self, label: str, celsius: float) -> None:
        self._label = label
        self.celsius = celsius  # очаткове значення теж перевіряє setter.

    @property
    def celsius(self) -> float:
        return self.__celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Температура має бути числом int або float.")
        if not self.MIN_CELSIUS <= value <= self.MAX_CELSIUS:
            raise ValueError(f"іапазон датчика: від {self.MIN_CELSIUS} до {self.MAX_CELSIUS} °C.")
        self.__celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32

    def reading(self) -> str:
        return f"{self._label}: {self.celsius:.1f} °C = {self.fahrenheit:.1f} °F"


def demo() -> None:
    sensor = TemperatureSensor("атчик 01", 20)
    print("очаткове значення:", sensor.reading())
    sensor.celsius = 25
    print("ісля sensor.celsius = 25:", sensor.reading())
    for invalid in ("25", 151):
        try:
            sensor.celsius = invalid
        except (TypeError, ValueError) as error:
            print(f"начення {invalid!r} → {type(error).__name__}: {error}")
    print("ісля відхилення значень:", sensor.reading())
    try:
        print(sensor.__celsius)
    except AttributeError:
        print("рямий доступ sensor.__celsius → AttributeError")
    print("Name mangling: sensor._TemperatureSensor__celsius =",
          sensor._TemperatureSensor__celsius)
