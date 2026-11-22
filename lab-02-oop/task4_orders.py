"""бстрактний контракт способу доставки і композиція замовлення."""

from abc import ABC, abstractmethod


class ShippingMethod(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """азва способу доставки."""

    @abstractmethod
    def cost(self, weight_g: int) -> int:
        """артість доставки в гривнях."""

    @abstractmethod
    def days(self, distance_km: int) -> int:
        """Строк у днях."""

    def describe(self, weight_g: int, distance_km: int) -> str:
        return f"{self.name}: доставка {self.cost(weight_g)} грн, строк {self.days(distance_km)} дн."


class StorePickup(ShippingMethod):
    @property
    def name(self) -> str:
        return "Самовивіз"

    def cost(self, weight_g: int) -> int:
        return 0

    def days(self, distance_km: int) -> int:
        return 1


class CourierDelivery(ShippingMethod):
    @property
    def name(self) -> str:
        return "ур'єр"

    def cost(self, weight_g: int) -> int:
        started_kilograms = (weight_g + 999) // 1_000
        return 60 + 10 * started_kilograms

    def days(self, distance_km: int) -> int:
        return 1 if distance_km <= 20 else 2


class OrderItem:
    def __init__(self, title: str, price_uah: int, weight_g: int, quantity: int) -> None:
        if type(price_uah) is not int or price_uah < 0:
            raise ValueError("іну задають невід'ємним цілим числом у гривнях.")
        if type(weight_g) is not int or weight_g <= 0:
            raise ValueError("агу задають додатним цілим числом у грамах.")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("ількість має бути додатним цілим числом.")
        self.title = title
        self.price_uah = price_uah
        self.weight_g = weight_g
        self.quantity = quantity

    def line_price(self) -> int:
        return self.price_uah * self.quantity

    def line_weight(self) -> int:
        return self.weight_g * self.quantity


class Order:
    def __init__(self, items: list[OrderItem], shipping: ShippingMethod, distance_km: int) -> None:
        if not items:
            raise ValueError("одайте хоча б одну позицію замовлення.")
        if type(distance_km) is not int or distance_km < 0:
            raise ValueError("ідстань задають невід'ємним цілим числом у кілометрах.")
        self.items = tuple(items)
        self.shipping = shipping
        self.distance_km = distance_km

    def subtotal(self) -> int:
        return sum(item.line_price() for item in self.items)

    def weight(self) -> int:
        return sum(item.line_weight() for item in self.items)

    def total(self) -> int:
        return self.subtotal() + self.shipping.cost(self.weight())

    def shipping_summary(self) -> str:
        return self.shipping.describe(self.weight(), self.distance_km)


def demo() -> None:
    try:
        ShippingMethod()
    except TypeError:
        print("ShippingMethod() → TypeError: абстрактний клас.")

    items = [OrderItem("нига", 240, 450, 2), OrderItem("локнот", 90, 200, 1)]
    print("амовлення")
    for item in items:
        print(f"  {item.title}: {item.quantity} шт. × {item.price_uah} грн = {item.line_price()} грн")
    for method in [StorePickup(), CourierDelivery()]:
        order = Order(items, method, distance_km=35)
        print(f"\n{type(method).__name__}: товари {order.subtotal()} грн, вага {order.weight()} г")
        print("  " + order.shipping_summary())
        print(f"  о сплати: {order.total()} грн")
