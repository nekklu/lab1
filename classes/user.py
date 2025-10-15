from booking import Booking

class User:
    def __init__(self, user_id: int, name: str, contact_info: str):
        #Прописываеём проверки типов и значений
        if not isinstance(user_id, int):
            raise TypeError("ID пользователя должен быть целым числом.")
        if not isinstance(name, str):
            raise TypeError("Имя пользователя должно быть строкой.")
        if not isinstance(contact_info, str):
            raise TypeError("Контактная информация должна быть строкой.")
        
        if user_id <= 0:
            raise ValueError("ID пользователя должен быть положительным числом.")
        if not name:
            raise ValueError("Имя пользователя не может быть пустым.")
        if not contact_info:
            raise ValueError("Контактная информация не может быть пустой.")
        
        #Присваиваем значения атрибутам класса
        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info
        #Получаем список бронирований
        self.bookings: list['Booking'] = []
    
    #Возвращаем информацию об обьекте
    def __str__(self):
        return f"Пользователь: {self.name} (ID: {self.user_id})"