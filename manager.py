import json
from classes import Address, User, Housing, Booking, Review

class DataManager:

    def __init__(self):
        self.users = []
        self.housings = []
        self.bookings = []
        self.reviews = []

    def add_user(self, user: User):
        self.users.append(user)

    def add_housing(self, housing: Housing):
        self.housings.append(housing)
    

    def get_user_by_id(self, user_id: int) -> User | None:
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_housing_by_id(self, housing_id: int) -> Housing | None:
        for housing in self.housings:
            if housing.housing_id == housing_id:
                return housing
        return None

    # Update
    def update_user(self, user_id: int, new_data: dict) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in new_data.items():
                if hasattr(user, key):
                    setattr(user, key, value) 
            return True
        return False 

    # Delete
    def delete_user_by_id(self, user_id: int) -> bool:
        """Удаляет пользователя по ID."""
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False 

    def get_data_as_dict(self):
        return {
            "users": [u.__dict__ for u in self.users],
            "housings": [{'housing_id': h.housing_id, 'location': h.location.__dict__, 'price_per_night': h.price_per_night, 'description': h.description} for h in self.housings],
            "bookings": [{"booking_id": b.booking_id, "user_id": b.user.user_id, "housing_id": b.housing.housing_id, "start_date": b.start_date, "end_date": b.end_date,} for b in self.bookings],
            "reviews": [{"review_id": r.review_id, "user_id": r.user.user_id, "housing_id": r.housing_id, "rating": r.rating, "comment": r.comment} for r in self.reviews]
        }
    #Сохранение данных в JSON файл
    def save_to_json(self, filename: str):
        data = self.get_data_as_dict()
        for user in data['users']: user.pop('bookings', None)
        for house in data['housings']: house.pop('reviews', None)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {filename}")

    #Загрузка данных из JSON файла
    def load_from_json(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        try:
            self.users = [User(**u) for u in data['users']]
            self.housings = [Housing(housing_id=h['housing_id'], location=Address(**h['location']), price_per_night=h['price_per_night'], description=h['description']) for h in data['housings']]
            users_map = {u.user_id: u for u in self.users}; housings_map = {h.housing_id: h for h in self.housings}
            self.bookings = [Booking(b['booking_id'], users_map[b['user_id']], housings_map[b['housing_id']], b['start_date'], b['end_date']) for b in data['bookings']]
            self.reviews = [Review(r['review_id'], users_map[r['user_id']], housings_map[r['housing_id']], r['rating'], r['comment']) for r in data['reviews']]
            print(f"Данные успешно загружены из {filename}")
        except (KeyError, TypeError) as e:
            print(f"Ошибка при загрузке данных: {e}")