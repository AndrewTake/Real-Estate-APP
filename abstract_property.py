from sqlalchemy import Column, String, Integer, Float
from base import Base

from sqlalchemy import null


class AbstractProperty(Base):
    """ Represents a property """

    BOOLEAN_TRUE = 1

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    parcel_number = Column(String(100))
    street_name = Column(String(100))
    city = Column(String(100))
    postal_code = Column(String(100))
    purchase_price = Column(Float)
    selling_price = Column(Float)
    is_sold = Column(Integer)
    type = Column(String(10))

    def __init__(self, parcel_number, street_name, city, postal_code,
                 purchase_price, type):
        """ Initializes the Property """

        AbstractProperty.validate_string("Parcel Number", parcel_number)
        self.parcel_number = parcel_number

        AbstractProperty.validate_string("Street Name", street_name)
        self.street_name = street_name

        AbstractProperty.validate_string("City", city)
        self.city = city

        AbstractProperty.validate_string("Postal Code", postal_code)
        self.postal_code = postal_code

        AbstractProperty.validate_string("Purchase Price", purchase_price)
        self.purchase_price = purchase_price

        AbstractProperty.validate_string("Type", type)
        self.type = type

        self.is_sold = False
        self.selling_price = 0.0

    def calc_profit(self):
        """ Calculates the profit of property """

        if not self.is_sold:
            return 0.0

        return (self.purchase_price - self.selling_price)

    def mark_is_sold(self, selling_price):
        """ Called when a property is sold """

        AbstractProperty.validate_float(
            "Selling Price", selling_price)

        self.selling_price = selling_price
        self.is_sold = 1

    def sold(self):
        """ Returns a boolean indicating whether the property is sold """
        if self.is_sold == AbstractProperty.BOOLEAN_TRUE:
            return True

        return False

    def to_dict(self):
        """ Raises a non implemented error """

        raise NotImplementedError("Child class must implement")

    def get_details(self):
        """ Child must implement and return the correct type """

        raise NotImplementedError("Child class must implement")

    def get_type(self):
        """ Child must implement and return the correct type """

        raise NotImplementedError("Child class must implement")

    @staticmethod
    def validate_string(label, value):
        """ Values a string value """

        if value is None:
            raise ValueError(label + " must be defined.")
        if value == "":
            raise ValueError(label + " cannot be empty.")

    @staticmethod
    def validate_float(label, value):
        """ Values a string value """
        if value is None:
            raise ValueError(label + " must be defined.")
        if type(value) != float:
            raise ValueError(label + " must be a float.")
        if value < 0.0:
            raise ValueError(label + " must be positive.")

    @staticmethod
    def validate_int(label, value):
        """ Values a string value """
        if value is None:
            raise ValueError(label + " must be defined.")
        if type(value) != int:
            raise ValueError(label + " must be an integer.")
        if value < 0:
            raise ValueError(label + " must be positive.")
