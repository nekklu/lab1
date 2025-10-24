
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from classes import Address, User, Housing, Booking, Review

class Manager:
    """
    Статический класс-сервис, который отвечает только за сохранение (сериализацию)
    и загрузку (десериализацию) данных из файлов.
    """

    @staticmethod
    def save_to_json(filename: str):
        """Сохраняет текущее состояние всех объектов из классов в файл JSON."""
        # ... (код этого метода остается без изменений) ...
        data = {
            "users": [u.__dict__ for u in User.get_all()],
            "housings": [{'housing_id': h.housing_id, 'location': h.location.__dict__, 'price_per_night': h.price_per_night, 'description': h.description} for h in Housing.get_all()],
            "bookings": [{"booking_id": b.booking_id, "user_id": b.user.user_id, "housing_id": b.housing.housing_id, "start_date": b.start_date, "end_date": b.end_date} for b in Booking.get_all()],
            "reviews": [{"review_id": r.review_id, "user_id": r.user.user_id, "housing_id": r.housing.housing_id, "rating": r.rating, "comment": r.comment} for r in Review.get_all()]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Данные успешно сохранены в {filename}")

    @staticmethod
    def load_from_json(filename: str):
        """Загружает данные из файла JSON, полностью перезаписывая текущее состояние."""
        # ... (код этого метода остается без изменений) ...
        User.clear_all(); Housing.clear_all(); Booking.clear_all(); Review.clear_all()
        try:
            with open(filename, 'r', encoding='utf-8') as f: data = json.load(f)
            for u_data in data.get('users', []): User.create(**u_data)
            for h_data in data.get('housings', []):
                addr = Address(**h_data.pop('location'))
                Housing.create(location=addr, **h_data)
            user_map = {u.user_id: u for u in User.get_all()}
            housing_map = {h.housing_id: h for h in Housing.get_all()}
            for b_data in data.get('bookings', []):
                user = user_map.get(b_data.pop('user_id'))
                housing = housing_map.get(b_data.pop('housing_id'))
                if user and housing: Booking.create(user=user, housing=housing, **b_data)
            for r_data in data.get('reviews', []):
                user = user_map.get(r_data.pop('user_id'))
                housing = housing_map.get(r_data.pop('housing_id'))
                if user and housing: Review.create(user=user, housing=housing, **r_data)
            print(f"✅ Данные успешно загружены из {filename}")
        except FileNotFoundError:
            print(f"⚠️ Файл {filename} не найден. Загрузка не выполнена.")
        except json.JSONDecodeError:
            print(f"⚠️ Ошибка чтения файла {filename}. Возможно, он поврежден.")

    @staticmethod
    def save_to_xml(filename: str):
        """Сохраняет текущее состояние всех объектов из классов в файл XML."""
        # ... (код этого метода остается без изменений) ...
        root = ET.Element("data")
        users_el = ET.SubElement(root, "users")
        for u in User.get_all():
            user_el = ET.SubElement(users_el, "user", id=str(u.user_id))
            ET.SubElement(user_el, "name").text = u.name
            ET.SubElement(user_el, "contact_info").text = u.contact_info
        housings_el = ET.SubElement(root, "housings")
        for h in Housing.get_all():
            h_el = ET.SubElement(housings_el, "housing", id=str(h.housing_id), price=str(h.price_per_night))
            loc_el = ET.SubElement(h_el, "location")
            ET.SubElement(loc_el, "city").text = h.location.city
            ET.SubElement(loc_el, "street").text = h.location.street
            ET.SubElement(loc_el, "building_number").text = str(h.location.building_number)
            if h.location.postal_code: ET.SubElement(loc_el, "postal_code").text = str(h.location.postal_code)
            ET.SubElement(h_el, "description").text = h.description
        bookings_el = ET.SubElement(root, "bookings")
        for b in Booking.get_all():
            b_el = ET.SubElement(bookings_el, "booking", id=str(b.booking_id), user_id=str(b.user.user_id), housing_id=str(b.housing.housing_id))
            ET.SubElement(b_el, "start_date").text = b.start_date
            ET.SubElement(b_el, "end_date").text = b.end_date
        reviews_el = ET.SubElement(root, "reviews")
        for r in Review.get_all():
            r_el = ET.SubElement(reviews_el, "review", id=str(r.review_id), user_id=str(r.user.user_id), housing_id=str(r.housing.housing_id), rating=str(r.rating))
            ET.SubElement(r_el, "comment").text = r.comment
        xml_string = ET.tostring(root, 'utf-8')
        pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="    ")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        print(f"✅ Данные успешно сохранены в {filename}")

    @staticmethod
    def load_from_xml(filename: str):
        """Загружает данные из файла XML, полностью перезаписывая текущее состояние."""
        # ... (код этого метода остается без изменений) ...
        User.clear_all(); Housing.clear_all(); Booking.clear_all(); Review.clear_all()
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            for u_node in root.find('users'): User.create(user_id=int(u_node.get('id')), name=u_node.find('name').text, contact_info=u_node.find('contact_info').text)
            for h_node in root.find('housings'):
                loc_node = h_node.find('location')
                pc_node = loc_node.find('postal_code')
                address = Address(city=loc_node.find('city').text, street=loc_node.find('street').text, building_number=loc_node.find('building_number').text, postal_code=int(pc_node.text) if pc_node is not None else None)
                Housing.create(housing_id=int(h_node.get('id')), price_per_night=float(h_node.get('price')), description=h_node.find('description').text, location=address)
            user_map = {u.user_id: u for u in User.get_all()}
            housing_map = {h.housing_id: h for h in Housing.get_all()}
            for b_node in root.find('bookings'):
                user = user_map.get(int(b_node.get('user_id')))
                housing = housing_map.get(int(b_node.get('housing_id')))
                if user and housing: Booking.create(booking_id=int(b_node.get('id')), user=user, housing=housing, start_date=b_node.find('start_date').text, end_date=b_node.find('end_date').text)
            for r_node in root.find('reviews'):
                user = user_map.get(int(r_node.get('user_id')))
                housing = housing_map.get(int(r_node.get('housing_id')))
                if user and housing: Review.create(review_id=int(r_node.get('id')), user=user, housing=housing, rating=int(r_node.get('rating')), comment=r_node.find('comment').text)
            print(f"✅ Данные успешно загружены из {filename}")
        except FileNotFoundError:
            print(f"⚠️ Файл {filename} не найден. Загрузка не выполнена.")
        except ET.ParseError:
            print(f"⚠️ Ошибка чтения файла {filename}. Возможно, он поврежден.")