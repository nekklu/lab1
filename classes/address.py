# Кастомное исключение для ошибок, связанных с адресом
class AddressDataError(Exception):
    pass

class Address:
    def __init__(self, city: str, street: str, building_number: str, postal_code: int = None):
        if not isinstance(city, str) or not city:
            raise AddressDataError("Город должен быть непустой строкой.")
        if not isinstance(street, str) or not street:
            raise AddressDataError("Улица должна быть непустой строкой.")
        if not isinstance(building_number, str) or not building_number:
            raise AddressDataError("Номер дома должен быть непустой строкой.")
        if postal_code is not None and (not isinstance(postal_code, int) or postal_code <= 0):
            raise AddressDataError("Почтовый индекс должен быть положительным числом.")

        self.city = city
        self.street = street
        self.building_number = building_number
        self.postal_code = postal_code

    def __str__(self):
        address_parts = [self.city, self.street, self.building_number]
        if self.postal_code:
            address_parts.append(f"({self.postal_code})")
        return ", ".join(address_parts)