from address import Address
from review import Review

class Housing:
    def __init__(self, housing_id: int, location: Address, price_per_night: float, description: str):
        if not isinstance(housing_id, int):
            raise TypeError("ID жилья должен быть целым числом.")
        if not isinstance(location, Address):
            raise TypeError("Местоположение должно быть объектом класса Address.")
        if not isinstance(price_per_night, (int, float)):
            raise TypeError("Цена за ночь должна быть числом.")
        if not isinstance(description, str):
            raise TypeError("Описание должно быть строкой.")

        if housing_id <= 0:
            raise ValueError("ID жилья должен быть положительным числом.")
        if price_per_night <= 0:
            raise ValueError("Цена за ночь должна быть положительным числом.")

        self.housing_id = housing_id
        self.location = location
        self.price_per_night = price_per_night
        self.description = description
        self.reviews: list['Review'] = []

    def __str__(self):
        return f"Жилье (ID: {self.housing_id}): {self.location} | Цена: {self.price_per_night} за ночь | Отзывы: {len(self.reviews)}"