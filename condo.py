
from abstract_property import AbstractProperty
from sqlalchemy import Column, String, Integer, Float, DateTime, desc


class Condo(AbstractProperty):
    """ Represents a property """

    TYPE = "Condo"

    hoa_fee = Column(Integer)
    developer_name = Column(String(100))
    unit = Column(Integer)

    def __init__(self, parcel_number, street_name, city, postal_code,
                 purchase_price,
                 hoa_fee, developer_name, unit):

        super().__init__(parcel_number, street_name, city, postal_code,
                         purchase_price, Condo.TYPE)

        AbstractProperty.validate_int("HOA Fee", hoa_fee)
        self.hoa_fee = hoa_fee

        AbstractProperty.validate_string("Developer Name", developer_name)
        self.developer_name = developer_name

        AbstractProperty.validate_int("Unit Amount", unit)
        self.unit = unit

    def get_details(self):
        """ Returns the details of a property """
        description = "Parcel Number: %s, Address: %s, %s, %s. Developer Name: %s. HOA Fee: %d, Units: %d. " % \
            (self.parcel_number,
             self.street_name,
             self.city,
             self.postal_code,
             self.developer_name,
             self.hoa_fee,
             self.unit)

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
        properties["hoa_fee"] = self.hoa_fee
        properties["developer_name"] = self.developer_name
        properties["is_sold"] = self.sold()
        properties["unit"] = self.unit
        properties["type"] = self.TYPE

        return properties

    def get_type(self):
        """ Returns the type of this class """
        return Condo.TYPE
