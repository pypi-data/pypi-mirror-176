from abc import ABC, abstractmethod


class Apartment:
    def __init__(self, address, rent, bedrooms, bathrooms, link, available_date, agency, is_studio):
        self.address = address
        self.rent = rent
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.link = link
        self.available_date = available_date
        self.agency = agency
        self.is_studio = is_studio

    def __str__(self):
        return f"'{self.address}' -- ${self.rent} {self.bedrooms}BED/{self.bathrooms}BATH {self.available_date} {self.link}"
    __repr__ = __str__


class BaseAgency(ABC):
    @abstractmethod
    def get_all(self):
        pass
