"""аслідування і поліморфізм на прикладі транспорту."""

from math import isfinite


class Vehicle:
    def __init__(self, name: str, speed_kmh: float) -> None:
        if not isfinite(speed_kmh) or speed_kmh <= 0:
            raise ValueError("Швидкість має бути скінченним додатним числом.")
        self.name = name
        self.speed_kmh = speed_kmh

    def trip_minutes(self, distance_km: float) -> float:
        if not isfinite(distance_km) or distance_km < 0:
            raise ValueError("ідстань має бути скінченною і невід'ємною.")
        return 60 * distance_km / self.speed_kmh

    def __str__(self) -> str:
        return f"{self.name} (базова швидкість {self.speed_kmh:g} км/год)"


class Bicycle(Vehicle):
    def __init__(self, name: str, speed_kmh: float, cargo_kg: float) -> None:
        super().__init__(name, speed_kmh)
        if not isfinite(cargo_kg) or cargo_kg < 0:
            raise ValueError("аса вантажу має бути скінченною і невід'ємною.")
        self.cargo_kg = cargo_kg

    def trip_minutes(self, distance_km: float) -> float:
        #  навчальній моделі 20 кг вантажу подвоюють час поїздки.
        return super().trip_minutes(distance_km) * (1 + self.cargo_kg / 20)


class ElectricScooter(Vehicle):
    def __init__(self, name: str, speed_kmh: float, range_km: float) -> None:
        super().__init__(name, speed_kmh)
        if not isfinite(range_km) or range_km <= 0:
            raise ValueError("апас ходу має бути скінченним і додатним.")
        self.range_km = range_km

    def trip_minutes(self, distance_km: float) -> float:
        minutes = super().trip_minutes(distance_km)
        if distance_km > self.range_km:
            raise ValueError(f"апас ходу {self.range_km:g} км недостатній.")
        return minutes


class Van(Vehicle):
    def __init__(self, name: str, speed_kmh: float, loading_minutes: float) -> None:
        super().__init__(name, speed_kmh)
        if not isfinite(loading_minutes) or loading_minutes < 0:
            raise ValueError("ас завантаження має бути скінченним і невід'ємним.")
        self.loading_minutes = loading_minutes

    def trip_minutes(self, distance_km: float) -> float:
        return super().trip_minutes(distance_km) + self.loading_minutes


def demo() -> None:
    bicycle = Bicycle("елосипед", 20, 5)
    scooter = ElectricScooter("лектросамокат", 24, 15)
    van = Van("ургон", 40, 8)
    vehicles = [bicycle, scooter, van]
    distance_km = 12
    print(f"ідстань маршруту: {distance_km} км.")
    print("антаж велосипеда: 5 кг. апас ходу самоката: 15 км.")
    print("авантаження фургона: 8 хв.")
    for vehicle in vehicles:
        print(f"{vehicle}: {vehicle.trip_minutes(distance_km):.2f} хв")
    print("isinstance(bicycle, Vehicle):", isinstance(bicycle, Vehicle))
    print("issubclass(ElectricScooter, Vehicle):", issubclass(ElectricScooter, Vehicle))
    print("isinstance(van, Bicycle):", isinstance(van, Bicycle))
    try:
        scooter.trip_minutes(16)
    except ValueError as error:
        print("Самокат, маршрут 16 км:", error)
