from classes import Address, User, Housing
from manager import Manager

def main():
    manager = Manager()

    print("1. Операция CREATE")
    user1 = User(1, "Иван Петров", "ivan.p@example.com")
    user2 = User(2, "Анна Смирнова", "anna.s@example.com")
    address1 = Address(city="Москва", street="Тверская", building_number="10", postal_code=125009)
    house1 = Housing(101, address1, 5500, "Уютная квартира в центре")
    
    # Используем методы 'add' вместо прямого '.append()'
    manager.add_user(user1)
    manager.add_user(user2)
    manager.add_housing(house1)
    
    print(f"✅ Создано пользователей: {len(manager.users)}")
    print(f"✅ Создано объектов жилья: {len(manager.housings)}")
    
    # Используем метод для чтения данных
    print("\n2. Операция READ")
    retrieved_user = manager.get_user_by_id(1)
    if retrieved_user:
        print(f"   Найден пользователь по ID=1: {retrieved_user.name}")
    else:
        print("   Пользователь по ID=1 не найден.")
    
    
    print("\n3. Операция UPDATE")
    print(f"   Имя пользователя (ID=1) до обновления: {manager.get_user_by_id(1).name}")
    
    # Используем метод update для изменения данных
    update_data = {'name': "Иван 'Обновленный' Петров", 'contact_info': 'ivan.new@example.com'}
    success = manager.update_user(1, update_data)
    
    if success:
        print(f"   Имя пользователя (ID=1) после обновления: {manager.get_user_by_id(1).name}")
        print(f"   Контакт (ID=1) после обновления: {manager.get_user_by_id(1).contact_info}")
    else:
        print("   Не удалось обновить пользователя.")

    print("\n4. Операция DELETE")
    print(f"   Количество пользователей до удаления: {len(manager.users)}")
    
    # Используем метод 'delete' для удаления объекта
    deleted = manager.delete_user_by_id(2) # Удаляем пользователя с ID=2
    
    if deleted:
        print(f"   Пользователь с ID=2 успешно удален.")
        print(f"   Количество пользователей после удаления: {len(manager.users)}")
    else:
        print(f"   Не удалось удалить пользователя с ID=2.")
        
    print("\n5. Сохранение итоговых данных")
    # После всех операций сохраняем итоговое состояние в файл
    manager.save_to_json("crud_data.json")

if __name__ == '__main__':
    main()