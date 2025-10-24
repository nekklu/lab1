# Кастомное исключение для ошибок, связанных с пользователем
class UserDataError(Exception):
    pass

class User:
    def __init__(self, user_id: int, name: str, contact_info: str):
        if not isinstance(user_id, int) or user_id <= 0:
            raise UserDataError("ID пользователя должен быть положительным целым числом.")
        if not isinstance(name, str) or not name:
            raise UserDataError("Имя пользователя не может быть пустым.")
        if not isinstance(contact_info, str) or not contact_info:
            raise UserDataError("Контактная информация не может быть пустой.")

        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info
        # В этой версии мы не храним бронирования прямо в пользователе,
        # чтобы избежать цикличных ссылок при сохранении. Менеджер будет управлять связями.
        # self.bookings: list['Booking'] = []

    def __str__(self):
        return f"Пользователь: {self.name} (ID: {self.user_id})"