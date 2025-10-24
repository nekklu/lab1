# manager.py
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom  # Используется для красивой записи XML

# Импортируем все необходимые классы из нашего пакета `classes`
from classes import Address, User, Housing, Booking, Review

class Manager:
    """
    Класс Manager управляет всеми данными в системе: пользователями, жильем,
    бронированиями и отзывами. Реализует CRUD-операции и сериализацию/десериализацию
    данных в форматы JSON и XML.
    """
    def __init__(self):
        self.users: list[User] = []
        self.housings: list[Housing] = []
        self.bookings: list[Booking] = []
        self.reviews: list[Review] = []

    # --- Операции CRUD (Create, Read, Delete) ---

    def add_user(self, user: User): self.users.append(user)
    def add_housing(self, housing: Housing): self.housings.append(housing)
    def add_booking(self, booking: Booking): self.bookings.append(booking)
    def add_review(self, review: Review): self.reviews.append(review)

    def get_user_by_id(self, user_id: int) -> User | None:
        """Находит пользователя по ID. Возвращает None, если не найден."""
        return next((u for u in self.users if u.user_id == user_id), None)

    def get_housing_by_id(self, housing_id: int) -> Housing | None:
        """Находит жилье по ID. Возвращает None, если не найдено."""
        return next((h for h in self.housings if h.housing_id == housing_id), None)
    
    def update_user(self, user_id: int, new_data: dict) -> bool:
        """
        Обновляет данные пользователя по его ID.
        new_data - словарь, где ключ - имя атрибута, а значение - новое значение.
        """
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in new_data.items():
                # Проверяем, есть ли такой атрибут у объекта, чтобы не создать лишний
                if hasattr(user, key):
                    setattr(user, key, value)
            return True
        return False # Пользователь не найден
        
    def delete_user_by_id(self, user_id: int) -> bool:
        """Удаляет пользователя и все связанные с ним данные (бронирования, отзывы)."""
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            # Важно: удаляем связанные данные для сохранения целостности
            self.bookings = [b for b in self.bookings if b.user.user_id != user_id]
            self.reviews = [r for r in self.reviews if r.user.user_id != user_id]
            return True
        return False

    # --- Работа с JSON ---

    def save_to_json(self, filename: str):
        """Сохраняет все данные в файл формата JSON."""
        data = {
            "users": [u.__dict__ for u in self.users],
            "housings": [
                {
                    'housing_id': h.housing_id,
                    'location': h.location.__dict__, # Преобразуем объект Address в словарь
                    'price_per_night': h.price_per_night,
                    'description': h.description
                } for h in self.housings
            ],
            "bookings": [
                {
                    "booking_id": b.booking_id,
                    "user_id": b.user.user_id, # Сохраняем только ID для связи
                    "housing_id": b.housing.housing_id, # Сохраняем только ID для связи
                    "start_date": b.start_date,
                    "end_date": b.end_date
                } for b in self.bookings
            ],
            "reviews": [
                {
                    "review_id": r.review_id,
                    "user_id": r.user.user_id,
                    "housing_id": r.housing.housing_id,
                    "rating": r.rating,
                    "comment": r.comment
                } for r in self.reviews
            ]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename: str):
        """Загружает все данные из файла формата JSON."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 1. Создаем базовые объекты
        self.users = [User(**u_data) for u_data in data.get('users', [])]
        self.housings = [Housing(location=Address(**h_data['location']), **{k: v for k, v in h_data.items() if k != 'location'}) for h_data in data.get('housings', [])]
        
        # 2. Создаем словари для быстрого поиска объектов по ID, чтобы восстановить связи
        user_map = {u.user_id: u for u in self.users}
        housing_map = {h.housing_id: h for h in self.housings}

        # 3. Создаем объекты со связями
        self.bookings = [Booking(user=user_map[b_data['user_id']], housing=housing_map[b_data['housing_id']], **{k: v for k, v in b_data.items() if k not in ['user_id', 'housing_id']}) for b_data in data.get('bookings', [])]
        self.reviews = [Review(user=user_map[r_data['user_id']], housing=housing_map[r_data['housing_id']], **{k: v for k, v in r_data.items() if k not in ['user_id', 'housing_id']}) for r_data in data.get('reviews', [])]

    # --- Работа с XML ---

    def save_to_xml(self, filename: str):
        """Сохраняет все данные в файл формата XML."""
        root = ET.Element("data")
        
        users_el = ET.SubElement(root, "users")
        for u in self.users:
            user_el = ET.SubElement(users_el, "user", id=str(u.user_id))
            ET.SubElement(user_el, "name").text = u.name
            ET.SubElement(user_el, "contact_info").text = u.contact_info

        housings_el = ET.SubElement(root, "housings")
        for h in self.housings:
            h_el = ET.SubElement(housings_el, "housing", id=str(h.housing_id), price=str(h.price_per_night))
            loc_el = ET.SubElement(h_el, "location")
            ET.SubElement(loc_el, "city").text = h.location.city
            ET.SubElement(loc_el, "street").text = h.location.street
            ET.SubElement(loc_el, "building_number").text = str(h.location.building_number)
            if h.location.postal_code:
                ET.SubElement(loc_el, "postal_code").text = str(h.location.postal_code)
            ET.SubElement(h_el, "description").text = h.description

        bookings_el = ET.SubElement(root, "bookings")
        for b in self.bookings:
            b_el = ET.SubElement(bookings_el, "booking", id=str(b.booking_id), user_id=str(b.user.user_id), housing_id=str(b.housing.housing_id))
            ET.SubElement(b_el, "start_date").text = b.start_date
            ET.SubElement(b_el, "end_date").text = b.end_date

        # Сериализация отзывов (аналогично бронированиям)
        reviews_el = ET.SubElement(root, "reviews")
        for r in self.reviews:
            r_el = ET.SubElement(reviews_el, "review", id=str(r.review_id), user_id=str(r.user.user_id), housing_id=str(r.housing.housing_id), rating=str(r.rating))
            ET.SubElement(r_el, "comment").text = r.comment

        # Преобразование в строку с отступами для читаемости
        xml_string = ET.tostring(root, 'utf-8')
        pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="    ")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

    def load_from_xml(self, filename: str):
        """Загружает все данные из файла формата XML."""
        tree = ET.parse(filename)
        root = tree.getroot()

        # 1. Загружаем пользователей
        self.users = [
            User(user_id=int(u.get('id')), name=u.find('name').text, contact_info=u.find('contact_info').text)
            for u in root.find('users')
        ]
        
        # 2. Загружаем жилье
        self.housings = []
        for h in root.find('housings'):
            loc = h.find('location')
            pc_node = loc.find('postal_code')
            address = Address(
                city=loc.find('city').text,
                street=loc.find('street').text,
                building_number=loc.find('building_number').text,
                postal_code=int(pc_node.text) if pc_node is not None else None
            )
            self.housings.append(Housing(
                housing_id=int(h.get('id')),
                price_per_night=float(h.get('price')),
                description=h.find('description').text,
                location=address
            ))
        
        # 3. Создаем карты для восстановления связей
        user_map = {u.user_id: u for u in self.users}
        housing_map = {h.housing_id: h for h in self.housings}

        # 4. Загружаем бронирования и восстанавливаем связи
        self.bookings = [
            Booking(
                booking_id=int(b.get('id')),
                user=user_map[int(b.get('user_id'))],
                housing=housing_map[int(b.get('housing_id'))],
                start_date=b.find('start_date').text,
                end_date=b.find('end_date').text
            ) for b in root.find('bookings')
        ]

        # 5. Загружаем отзывы и восстанавливаем связи
        self.reviews = [
            Review(
                review_id=int(r.get('id')),
                user=user_map[int(r.get('user_id'))],
                housing=housing_map[int(r.get('housing_id'))],
                rating=int(r.get('rating')),
                comment=r.find('comment').text
            ) for r in root.find('reviews')
        ]