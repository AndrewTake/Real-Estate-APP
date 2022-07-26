
from abstract_property import AbstractProperty
from condo import Condo
from duplex import Duplex
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PropertyManager:
    """ Manages properties that are being bought or sold """

    def __init__(self, portfolio_name, db_name):
        """ Constructor for the properties """
        if portfolio_name is None or not isinstance(portfolio_name, str):
            raise ValueError("Invalid Store Name.")
        self._portfolio_name = portfolio_name
        self._next_id_num = 0

        if db_name is None or db_name == "":
            raise ValueError("DB Name cannot be undefined")
        engine = create_engine("sqlite:///" + db_name)
        self._db_session = sessionmaker(bind=engine)

    def get_portfolio_name(self):
        """ Returns the portfolio name """
        return self._portfolio_name

    def property_exists(self, parcel_number):
        """ Returns True if the property exists, False otherwise """
        if parcel_number is None or not isinstance(parcel_number, str):
            raise ValueError("Invalid Parcel Number.")
        session = self._db_session()
        property = session.query(AbstractProperty).filter(
            AbstractProperty.parcel_number == parcel_number).first()
        session.close()
        if property is not None:
            return True
        return False

    def add_property(self, property):
        """ Adds a new property """

        if property is None or not isinstance(property, AbstractProperty):
            raise ValueError("Invalid Property.")
            # Verify no duplicated Parcel Number
        if self.property_exists(property.parcel_number):
            raise ValueError("Parcel Number already exists.")
        session = self._db_session()
        session.add(property)
        session.commit()
        session.close()

    def get_property_by_parcel_num(self, parcel_number):
        """ Returns a property object with the given parcel number. """
        if parcel_number is None or not isinstance(parcel_number, str):
            raise ValueError("Invalid Parcel Number.")
        session = self._db_session()
        property = session.query(Condo).filter(Condo.parcel_number ==
                                               parcel_number).first()
        if property is None:
            property = session.query(Duplex).filter(Duplex.parcel_number ==

                                                    parcel_number).first()
        session.close()
        return property

    def delete_property_by_parcel_num(self, parcel_number):
        """ Deletes a property based off the parcel number. """
        if parcel_number is None or not isinstance(parcel_number, str):
            raise ValueError("Invalid Parcel Number.")
        session = self._db_session()
        property = session.query(AbstractProperty).filter(
            AbstractProperty.parcel_number == parcel_number).first()

        if property is None:
            session.close()
            raise ValueError("Parcel Number does not exist.")
        session.delete(property)
        session.commit()
        session.close()

    def get_property_details(self, property_type):
        """ Returns all properties of a given type"""
        session = self._db_session()

        if property_type == Condo.TYPE:
            properties = session.query(Condo).filter(
                Condo.type == "Condo").all()

        elif property_type == Duplex.TYPE:
            properties = session.query(Duplex).filter(
                Duplex.type == "Duplex").all()
        else:
            properties = []

        session.close()
        details_list = []

        for property in properties:
            details_list.append(property.get_details())

        return details_list

    def update_property(self, parcel_number, selling_price):
        """ Marks a property as sold. """
        session = self._db_session()

        property = session.query(Condo).filter(
            Condo.parcel_number == parcel_number).first()

        if property is None:
            property = (
                session.query(Duplex).filter(
                    Duplex.parcel_number == Duplex).first()
            )

        if property is None:
            raise ValueError("Could not find property by parcel number")
        property.mark_is_sold(selling_price)
        session.commit()

        session.close()

    @staticmethod
    def _validate_string_input(display_name, str_value):
        """ Private method used to validate String Values """

        if str_value is None:
            raise ValueError(display_name + " must be defined.")

        if str_value == "":
            raise ValueError(display_name + " cannot be empty.")

    @staticmethod
    def _validate_int_input(label, value):
        """ Private method validate int value """
        if value is None:
            raise ValueError(label + " must be defined.")
        if type(value) != int:
            raise ValueError(label + " must be an integer.")
        if value < 0:
            raise ValueError(label + " must be positive.")
