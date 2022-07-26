
from abstract_property import AbstractProperty
from sqlalchemy import Column, String, Integer, Float, DateTime


class Duplex(AbstractProperty):
    """ Represents a property """

    TYPE = "Duplex"

    strata_fee = Column(Integer)
    square_footage = Column(Integer)
    number_active_tenants = Column(Integer)

    def __init__(self, parcel_number, street_name, city, postal_code,
                 purchase_price,
                 strata_fee, square_footage, number_active_tenants):

        super().__init__(parcel_number, street_name, city, postal_code,
                         purchase_price, Duplex.TYPE)

        AbstractProperty.validate_int("Strata Fee", strata_fee)
        self.strata_fee = strata_fee

        AbstractProperty.validate_string("Square Footage", square_footage)
        self.square_footage = square_footage

        AbstractProperty.validate_int(
            "Number Active Tenants", number_active_tenants)
        self.number_active_tenants = number_active_tenants

    def get_details(self):
        """ Returns the details of a property """
        description = "Parcel Number: %s, Address: %s, %s, %s. Strata Fee: %d. Square Footage: %d. \
            Number of Active Tenants: %d." % \
            (self.parcel_number,
             self.street_name,
             self.city,
             self.postal_code,
             self.strata_fee,
             self.square_footage,
             self.number_active_tenants)

        if self.is_sold:
            description = 'Sold! ' + description + \
                "Selling Price: " + str(self.selling_price)

        return description

    def to_dict(self):
        """ Returns the condo as a dictionary """
        properties = {}
        properties["parcel_number"] = self.parcel_number
        properties["street_name"] = self.street_name
        properties["city"] = self.city
        properties["postal_code"] = self.postal_code
        properties["purchase_price"] = self.purchase_price
        properties["selling_price"] = self.selling_price
        properties["strata_fee"] = self.strata_fee
        properties["square_footage"] = self.square_footage
        properties["is_sold"] = self.is_sold()
        properties["number_active_tenants"] = self.number_active_tenants
        properties["type"] = self.TYPE

        return properties

    def get_type(self):
        """ Returns the type of this class """
        return Duplex.TYPE
