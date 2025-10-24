#Файл нужен исключительно для обозначения папки как пакета, для возможности импорта из нее
from .address import Address
from .user import User
from .house import Housing
from .booking import Booking
from .review import Review, InvalidRatingError