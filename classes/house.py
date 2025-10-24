from .address import Address

# Кастомное исключение для ошибок, связанных с жильем
class HousingDataError(Exception):
    pass

class Housing:
    def __init__(self, housing_id: int, location: Address, price_per_night: float, description: str):
        if not isinstance(housing_id, int) or housing_id <= 0:
            raise HousingDataError("ID жилья должен быть положительным целым числом.")
        if not isinstance(location, Address):
            raise TypeError("Местоположение должно быть объектом класса Address.")
        if not isinstance(price_per_night, (int, float)) or price_per_night <= 0:
            raise HousingDataError("Цена за ночь должна быть положительным числом.")
        if not isinstance(description, str):
            raise TypeError("Описание должно быть строкой.")

        self.housing_id = housing_id
        self.location = location
        self.price_per_night = price_per_night
        self.description = description
        # self.reviews: list['Review'] = [] # Управляется менеджером

    def __str__(self):
        return f"Жилье (ID: {self.housing_id}): {self.location} | Цена: {self.price_per_night} за ночь"