from .user import User
from .house import Housing

class InvalidRatingError(ValueError):
    """Собственное исключение для недопустимого рейтинга."""
    pass

class Review:
    _instances = {}  # Внутриклассовое хранилище: {review_id: review_object}

    def __init__(self, review_id: int, user: User, housing: Housing, rating: int, comment: str):
        if not isinstance(review_id, int) or review_id <= 0:
            raise ValueError("ID отзыва должен быть положительным числом.")
        if not isinstance(user, User) or not isinstance(housing, Housing):
             raise TypeError("user и housing должны быть объектами своих классов.")
        if not (1 <= rating <= 5):
            raise InvalidRatingError("Рейтинг должен быть в диапазоне от 1 до 5.")

        self.review_id = review_id
        self.user = user
        self.housing = housing
        self.rating = rating
        self.comment = comment

    @classmethod
    def create(cls, review_id: int, user: User, housing: Housing, rating: int, comment: str):
        """CREATE: Создает объект отзыва и сохраняет его."""
        if review_id in cls._instances:
            raise ValueError(f"Отзыв с ID {review_id} уже существует.")
        
        review = cls(review_id, user, housing, rating, comment)
        cls._instances[review_id] = review
        return review

    @classmethod
    def get(cls, review_id: int):
        """READ: Находит отзыв по ID."""
        return cls._instances.get(review_id)

    def update(self, rating: int = None, comment: str = None):
        """UPDATE: Обновляет данные конкретного отзыва."""
        if rating is not None:
            if not (1 <= rating <= 5):
                raise InvalidRatingError("Рейтинг должен быть в диапазоне от 1 до 5.")
            self.rating = rating
        if comment is not None:
            self.comment = comment

    def delete(self):
        """DELETE: Удаляет отзыв. Каскадное удаление не требуется."""
        del self.__class__._instances[self.review_id]

    @classmethod
    def get_all(cls):
        """Вспомогательный метод для получения всех экземпляров."""
        return list(cls._instances.values())

    @classmethod
    def clear_all(cls):
        """Вспомогательный метод для очистки хранилища."""
        cls._instances.clear()

    def __str__(self):
        return f"Отзыв {self.rating}/5 от {self.user.name}: {self.comment}"