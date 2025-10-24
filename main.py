# main.py
from manager import Manager
# Импортируем все классы и их кастомные исключения из пакета classes
from classes import *

def create_initial_data():
    """Создает набор данных по умолчанию, если не удалось загрузить из файла."""
    print("--- Создание набора данных по умолчанию ---")
    try:
        user1 = User.create(1, "Иван Петров", "ivan.p@example.com")
        user2 = User.create(2, "Анна Смирнова", "anna.s@example.com")
        user3 = User.create(3, "Олег Волков", "oleg.v@example.com")
        
        addr1 = Address(city="Москва", street="Тверская", building_number="10", postal_code=125009)
        addr2 = Address(city="Санкт-Петербург", street="Невский проспект", building_number="25")
        
        house1 = Housing.create(101, addr1, 5500, "Уютная квартира в центре Москвы")
        house2 = Housing.create(202, addr2, 4800, "Апартаменты с видом на Невский")
        
        Booking.create(501, user1, house1, "2024-01-10", "2024-01-15")
        Review.create(1001, user1, house1, 5, "Отличное место!")
        
        print("✅ Набор данных по умолчанию успешно создан.")
    except (ValueError, UserDataError, HousingDataError) as e:
        print(f"🔥 Произошла ошибка при создании данных по умолчанию: {e}")


def main():
    """
    Главная функция: сначала пытается загрузить данные, затем демонстрирует
    все возможности системы и в конце сохраняет результат.
    """
    print("--- Запуск программы: Попытка загрузки данных из JSON ---")
    Manager.load_from_json('data.json')

    # Проверяем, были ли данные загружены. Если нет - создаем их.
    if not User.get_all():
        print("⚠️ Данные не найдены или файл пуст.")
        create_initial_data()

    print("\n--- 1. Демонстрация расширенной обработки исключений ---")
    test_user = User.get(1)
    test_house = Housing.get(101)
    try:
        print("Попытка создать пользователя с некорректным ID...")
        User.create(-5, "Призрак", "ghost@mail.com")
    except UserDataError as e:
        print(f"✅ Поймана ошибка: {e}")
    try:
        print("Попытка создать отзыв с недопустимым рейтингом...")
        Review.create(9999, test_user, test_house, 0, "Слишком низкая оценка")
    except InvalidRatingError as e:
        print(f"✅ Поймана ошибка: {e}")
    try:
        print("Попытка создать пользователя с дублирующимся ID...")
        User.create(1, "Двойник Ивана", "fake@mail.com")
    except ValueError as e:
        print(f"✅ Поймана ошибка: {e}")
    
    print("\n--- 2. Демонстрация READ ---")
    print(f"Всего пользователей в системе: {len(User.get_all())}")

    print(f"\n--- 3. Демонстрация UPDATE ---")
    user_to_update = User.get(1)
    if user_to_update:
        print(f"Имя пользователя ID=1 до обновления: {user_to_update.name}")
        user_to_update.update(name="Иван 'Измененный' Петров")
        print(f"Имя пользователя ID=1 после обновления: {user_to_update.name}")
    
    print("\n--- 4. Демонстрация DELETE ---")
    user_to_delete = User.get(3)
    if user_to_delete:
        print(f"Пользователей до удаления: {len(User.get_all())}")
        original_name = user_to_delete.name
        user_to_delete.delete()
        print(f"✅ Пользователь '{original_name}' удален.")
        print(f"Пользователей после удаления: {len(User.get_all())}")
    
    print("\n--- 5. Сохранение и загрузка JSON ---")
    Manager.save_to_json('data.json')
    print("Загрузка данных из только что сохраненного JSON файла...")
    Manager.load_from_json('data.json')
    print("\nПроверка данных после загрузки из JSON:")
    review_from_json = Review.get(1001)
    if review_from_json:
        print(f"Комментарий из загруженного отзыва: '{review_from_json.comment}'")
    else:
        print("Отзыв 1001 не найден после загрузки из JSON.")

    print("\n--- 6. Сохранение и загрузка XML ---")
    # Сначала сохраняем текущее состояние (которое было загружено из JSON) в XML
    Manager.save_to_xml('data.xml')
    print("Загрузка данных из только что сохраненного XML файла...")
    # Имитируем перезапуск программы - загружаем данные из XML
    Manager.load_from_xml('data.xml')
    
    print("\nПроверка данных после загрузки из XML:")
    print(f"Количество объектов жилья в системе: {len(Housing.get_all())}")
    
    # Проверяем, что связи восстановились корректно, найдя бронирование
    booking_from_xml = Booking.get(501)
    if booking_from_xml:
        # Эта строка доказывает, что объекты Booking, User и Housing были
        # успешно загружены и правильно связаны друг с другом.
        print(f"Найдено бронирование пользователя '{booking_from_xml.user.name}' на жилье '{booking_from_xml.housing.description}'")
    else:
        print("Бронирование 501 не найдено после загрузки из XML.")


if __name__ == '__main__':
    main()