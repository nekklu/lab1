from .user import User
from .house import Housing

class BookingLogicError(Exception):
    """Собственное исключение для ошибок в логике бронирования."""
    pass

class Booking:
    _instances = {}  # Внутриклассовое хранилище: {booking_id: booking_object}

    def __init__(self, booking_id: int, user: User, housing: Housing, start_date: str, end_date: str):
        if not isinstance(booking_id, int) or booking_id <= 0:
            raise BookingLogicError("ID бронирования должен быть положительным числом.")
        if not isinstance(user, User):
            raise TypeError("Аргумент 'user' должен быть объектом класса User.")
        if not isinstance(housing, Housing):
            raise TypeError("Аргумент 'housing' должен быть объектом класса Housing.")
        if not start_date or not end_date:
            raise BookingLogicError("Даты начала и окончания не могут быть пустыми.")

        self.booking_id = booking_id
        self.user = user
        self.housing = housing
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def create(cls, booking_id: int, user: User, housing: Housing, start_date: str, end_date: str):
        """CREATE: Создает объект бронирования и сохраняет его."""
        if booking_id in cls._instances:
            raise ValueError(f"Бронирование с ID {booking_id} уже существует.")
        
        booking = cls(booking_id, user, housing, start_date, end_date)
        cls._instances[booking_id] = booking
        return booking

    @classmethod
    def get(cls, booking_id: int):
        """READ: Находит бронирование по ID."""
        return cls._instances.get(booking_id)

    def update(self, start_date: str = None, end_date: str = None):
        """UPDATE: Обновляет даты конкретного бронирования."""
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date

    def delete(self):
        """DELETE: Удаляет бронирование. Каскадное удаление не требуется."""
        del self.__class__._instances[self.booking_id]

    @classmethod
    def get_all(cls):
        """Вспомогательный метод для получения всех экземпляров."""
        return list(cls._instances.values())

    @classmethod
    def clear_all(cls):
        """Вспомогательный метод для очистки хранилища."""
        cls._instances.clear()

    def __str__(self):
        return f"Бронь #{self.booking_id}: {self.user.name} -> жилье {self.housing.housing_id}"