class UserDataError(Exception):
    """Собственное исключение для ошибок в данных пользователя."""
    pass

class User:
    _instances = {}  # Внутриклассовое хранилище: {user_id: user_object}

    def __init__(self, user_id: int, name: str, contact_info: str):
        # Проверки корректности данных для одного объекта
        if not isinstance(user_id, int) or user_id <= 0:
            raise UserDataError("ID пользователя должен быть положительным целым числом.")
        if not isinstance(name, str) or not name:
            raise UserDataError("Имя пользователя не может быть пустым.")
        if not isinstance(contact_info, str) or not contact_info:
            raise UserDataError("Контактная информация не может быть пустой.")
            
        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info

    @classmethod
    def create(cls, user_id: int, name: str, contact_info: str):
        """CREATE: Создает объект пользователя и сохраняет его в хранилище класса."""
        if user_id in cls._instances:
            raise ValueError(f"Пользователь с ID {user_id} уже существует.")
        
        user = cls(user_id, name, contact_info)  # Вызов __init__ для валидации
        cls._instances[user_id] = user
        return user

    @classmethod
    def get(cls, user_id: int):
        """READ: Находит пользователя по ID."""
        return cls._instances.get(user_id)

    def update(self, name: str = None, contact_info: str = None):
        """UPDATE: Обновляет данные конкретного пользователя."""
        if name is not None:
            self.name = name
        if contact_info is not None:
            self.contact_info = contact_info

    def delete(self):
        """DELETE: Удаляет пользователя и все связанные с ним бронирования и отзывы."""
        from .booking import Booking
        from .review import Review

        # Каскадное удаление: сначала удаляем зависимые объекты
        for booking in list(Booking._instances.values()):
            if booking.user.user_id == self.user_id:
                booking.delete()
        
        for review in list(Review._instances.values()):
            if review.user.user_id == self.user_id:
                review.delete()
        
        # Удаляем сам объект пользователя
        del self.__class__._instances[self.user_id]

    @classmethod
    def get_all(cls):
        """Вспомогательный метод для получения всех экземпляров."""
        return list(cls._instances.values())
        
    @classmethod
    def clear_all(cls):
        """Вспомогательный метод для очистки хранилища (нужен для загрузки из файла)."""
        cls._instances.clear()

    def __str__(self):
        return f"Пользователь: {self.name} (ID: {self.user_id})"