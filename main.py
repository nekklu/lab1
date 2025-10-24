# main.py
from manager import Manager
# Импортируем все из пакета classes
from classes import *

def main():
    manager = Manager()

    print("--- 1. Операция CREATE ---")
    try:
        user1 = User(1, "Иван Петров", "ivan.p@example.com")
        user2 = User(2, "Анна Смирнова", "anna.s@example.com")
        address1 = Address(city="Москва", street="Тверская", building_number="10", postal_code=125009)
        house1 = Housing(101, address1, 5500, "Уютная квартира в центре")
        booking1 = Booking(1, user1, house1, "2024-01-10", "2024-01-15")
        review1 = Review(1001, user1, house1, 5, "Все было отлично!")

        manager.add_user(user1)
        manager.add_user(user2)
        manager.add_housing(house1)
        manager.add_booking(booking1)
        manager.add_review(review1)
        print("✅ Объекты успешно созданы.")
        
    except (AddressDataError, UserDataError, HousingDataError, InvalidRatingError) as e:
        print(f"🔥 Произошла ошибка при создании объектов: {e}")

    print(f"\n--- 2. Операция READ ---")
    retrieved_user = manager.get_user_by_id(1)
    print(f"Найден пользователь: {retrieved_user}")
    
    print(f"\n--- 3. Операция UPDATE ---")
    user_to_update_id = 1
    print(f"Имя пользователя (ID={user_to_update_id}) до обновления: {manager.get_user_by_id(user_to_update_id).name}")
    
    update_data = {'name': "Иван 'Обновленный' Петров", 'contact_info': 'ivan.new@example.com'}
    if manager.update_user(user_to_update_id, update_data):
        print("✅ Пользователь успешно обновлен.")
        updated_user = manager.get_user_by_id(user_to_update_id)
        print(f"Имя пользователя после обновления: {updated_user.name}")
        print(f"Новые контакты: {updated_user.contact_info}")
    else:
        print(f"🔥 Не удалось найти пользователя с ID={user_to_update_id} для обновления.")

    print("\n--- 4. Сохранение и загрузка в JSON ---")
    manager.save_to_json('data.json')
    print("💾 Данные сохранены в data.json")
    
    manager_from_json = Manager()
    manager_from_json.load_from_json('data.json')
    print("📂 Данные загружены из data.json")
    print(f"Проверка: Загружено {len(manager_from_json.bookings)} бронирований.")
    
    print("\n--- 5. Сохранение и загрузка в XML ---")
    manager.save_to_xml('data.xml')
    print("💾 Данные сохранены в data.xml")

    manager_from_xml = Manager()
    manager_from_xml.load_from_xml('data.xml')
    print("📂 Данные загружены из data.xml")
    print(f"Проверка: Загружено {len(manager_from_xml.reviews)} отзывов.")
    if manager_from_xml.reviews:
        print(f"Первый отзыв из XML: '{manager_from_xml.reviews[0].comment}'")

    print("\n--- 6. Операция DELETE ---")
    print(f"Пользователей до удаления: {len(manager.users)}")
    user_to_delete_id = 2
    if manager.delete_user_by_id(user_to_delete_id):
        print(f"✅ Пользователь с ID={user_to_delete_id} удален.")
    print(f"Пользователей после удаления: {len(manager.users)}")

if __name__ == '__main__':
    main()