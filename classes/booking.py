from .user import User
from .house import Housing

# Кастомное исключение для ошибок бронирования
class BookingLogicError(Exception):
    pass

class Booking:
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

    def __str__(self):
        return (f"Бронирование (ID: {self.booking_id}) для '{self.user.name}' "
                f"на жилье ID {self.housing.housing_id} с {self.start_date} по {self.end_date}")