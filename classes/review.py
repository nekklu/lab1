from .user import User
from .house import Housing

class InvalidRatingError(Exception):
    pass
class Review:
    def __init__(self, review_id: int, user: User, housing: Housing, rating: int, comment: str):
        if not isinstance(review_id, int):
            raise TypeError("ID отзыва должен быть целым числом.")
        if not isinstance(user, User):
            raise TypeError("Аргумент 'user' должен быть объектом класса User.")
        if not isinstance(housing, Housing):
            raise TypeError("Аргумент 'housing' должен быть объектом класса Housing.")
        if not isinstance(rating, int):
            raise TypeError("Рейтинг должен быть целым числом.")
        if not isinstance(comment, str):
            raise TypeError("Комментарий должен быть строкой.")

        if review_id <= 0:
            raise ValueError("ID отзыва должен быть положительным числом.")
        if not (1 <= rating <= 5):
            raise InvalidRatingError("Рейтинг должен быть в диапазоне от 1 до 5.")
        
        self.review_id = review_id
        self.user = user
        self.housing = housing
        self.rating = rating
        self.comment = comment
        
    def __str__(self):
        return (f"Отзыв #{self.review_id} от '{self.user.name}': "
                f"Оценка {self.rating}/5. Комментарий: '{self.comment}'")