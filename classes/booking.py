from user import User
from house import Housing

class Booking:
    def __init__(self, booking_id: int, user: User, housing: Housing, start_date: str, end_date: str):
        #Прописываеём проверки типов и значений
        if not isinstance(booking_id, int):
            raise TypeError("ID бронирования должен быть целым числом.")
        if not isinstance(user, User):
            raise TypeError("Аргумент 'user' должен быть объектом класса User.")
        if not isinstance(housing, Housing):
            raise TypeError("Аргумент 'housing' должен быть объектом класса Housing.")
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            raise TypeError("Даты должны быть строками.")
        
        if booking_id <= 0:
            raise ValueError("ID бронирования должен быть положительным числом.")
        if not start_date:
            raise ValueError("Дата начала не может быть пустой.")
        if not end_date:
            raise ValueError("Дата окончания не может быть пустой.")
        
        #Присваиваем значения атрибутам класса
        self.booking_id = booking_id
        self.user = user
        self.housing = housing
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        #Возвращаем информацию об обьекте
        return (f"Бронирование (ID: {self.booking_id}) для пользователя '{self.user.name}' "
                f"на жилье ID {self.housing.housing_id} с {self.start_date} по {self.end_date}")