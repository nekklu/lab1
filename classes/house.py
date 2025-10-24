from .address import Address

class HousingDataError(Exception):
    """Собственное исключение для ошибок в данных жилья."""
    pass

class Housing:
    _instances = {}  # Внутриклассовое хранилище: {housing_id: housing_object}

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

    @classmethod
    def create(cls, housing_id: int, location: Address, price_per_night: float, description: str):
        """CREATE: Создает объект жилья и сохраняет его."""
        if housing_id in cls._instances:
            raise ValueError(f"Жилье с ID {housing_id} уже существует.")
        
        house = cls(housing_id, location, price_per_night, description)
        cls._instances[housing_id] = house
        return house

    @classmethod
    def get(cls, housing_id: int):
        """READ: Находит жилье по ID."""
        return cls._instances.get(housing_id)

    def update(self, price_per_night: float = None, description: str = None):
        """UPDATE: Обновляет данные конкретного жилья."""
        if price_per_night is not None:
            self.price_per_night = price_per_night
        if description is not None:
            self.description = description

    def delete(self):
        """DELETE: Удаляет жилье и все связанные с ним бронирования и отзывы."""
        from .booking import Booking
        from .review import Review
        
        # Каскадное удаление
        for booking in list(Booking._instances.values()):
            if booking.housing.housing_id == self.housing_id:
                booking.delete()
        
        for review in list(Review._instances.values()):
            if review.housing.housing_id == self.housing_id:
                review.delete()
                
        del self.__class__._instances[self.housing_id]

    @classmethod
    def get_all(cls):
        """Вспомогательный метод для получения всех экземпляров."""
        return list(cls._instances.values())
        
    @classmethod
    def clear_all(cls):
        """Вспомогательный метод для очистки хранилища."""
        cls._instances.clear()

    def __str__(self):
        return f"Жилье (ID: {self.housing_id}): {self.location} | Цена: {self.price_per_night}"