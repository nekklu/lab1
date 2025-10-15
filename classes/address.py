class Address:
    def __init__(self, city: str, street: str, building_number: str, postal_code: int = None):
        #Прописываеём проверки типов и значений
        if not isinstance(city, str):
            raise TypeError("Город должен быть строкой.")
        if not isinstance(street, str):
            raise TypeError("Улица должна быть строкой.")
        if not isinstance(building_number, int):
            raise TypeError("Номер дома должен быть строкой, т.к может содержать буквы(корпус, строение).")
        if not isinstance(postal_code, int):
            raise TypeError("Почтовый индекс должен быть числом.")
        if postal_code is not None and not isinstance(postal_code, int):
            raise TypeError("Почтовый индекс должен быть целым числом.")

        if not city:
            raise ValueError("Название города не может быть пустым.")
        if not street:
            raise ValueError("Название улицы не может быть пустым.")
        if not building_number:
            raise ValueError("Номер дома не может быть пустым.")
        if postal_code is not None and postal_code <= 0:
            raise ValueError("Почтовый индекс должен быть положительным числом.")    

        self.city = city
        self.street = street
        self.building_number = building_number
        self.postal_code = postal_code

    def __str__(self):
        #Возвращаем информацию об обьекте и если присутсвует почтовый индекс, добавляем его 
        address_parts = [self.city, self.street, self.building_number]
        if self.postal_code:
            address_parts.append(f"({self.postal_code})")
        return ", ".join(address_parts)