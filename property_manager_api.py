from flask import Flask, request
from property_manager import PropertyManager
from condo import Condo
from duplex import Duplex


import json

app = Flask(__name__)

PROPERTY_MANAGER_DB = 'properties.sqlite'
property_manager = PropertyManager("Andrew's Portfolio",
                                   "properties.sqlite")


@app.route("/portfolio/properties", methods=["POST"])
def add_property():
    """ Add a property to the portfolio - either condo or a duplex """

    content = request.json

    try:
        if content["type"] == Condo.TYPE:
            condo = Condo(
                content["parcel_number"],
                content["street_name"],
                content["city"],
                content["postal_code"],
                content["purchase_price"],
                content["hoa_fee"],
                content["developer_name"],
                content["unit"]
            )
            property_manager.add_property(condo)

        elif content["type"] == Duplex.TYPE:
            duplex = Duplex(
                content["parcel_number"],
                content["street_name"],
                content["city"],
                content["postal_code"],
                content["purchase_price"],
                content["strata_fee"],
                content["square_footage"],
                content["number_active_tenants"]
            )
            property_manager.add_property(duplex)
        else:
            response = app.response_class(
                status=400,
                response="Invalid Property Type"
            )
            return response

        response = app.response_class(
            status=200,
            response="Added"
        )
        return response

    except ValueError as e:
        response = app.response_class(
            status=400,
            response=str(e)
        )
        return response

    except KeyError as e:
        response = app.response_class(
            status=400,
            response=str(e)
        )
        return response


@app.route("/portfolio/properties/<string:parcel_number>", methods=["GET"])
def get_property(parcel_number):
    """ Gets a property by the parcel number """
    try:
        property = property_manager.get_property_by_parcel_num(parcel_number)

        if property == None:
            response = app.response_class(
                status=404
            )
        else:

            response = app.response_class(
                status=200,
                response=json.dumps(property.to_dict()),
                mimetype='application/json'
            )

    except ValueError as e:
        response = app.response_class(
            status=400,
            response="Invalid Property Type"
        )
        return response

    return response


@app.route("/portfolio/properties/<string:parcel_number>", methods=["DELETE"])
def delete_property(parcel_number):
    """ Deletes a property based off the parcel number """
    try:
        property_manager.delete_property_by_parcel_num(parcel_number)

        if property_manager == None:
            response = app.response_class(
                status=404
            )
        else:
            response = app.response_class(
                status=200,
                response="Deleted"
            )

    except ValueError as e:
        response = app.response_class(
            status=400,
            response="Invalid Property Type"
        )
        return response

    return response


@app.route("/portfolio/properties/all", methods=["GET"])
def get_all_properties():
    """ Returns the properties in the portfolio """

    all_properties = property_manager.get_all_properties()
    properties = []
    for property in all_properties:
        properties.append(property.to_dict())

    response = app.response_class(
        status=200,
        response=json.dumps(properties),
        mimetype='application/json'
    )

    return response


@app.route("/portfolio/properties/all/<string:type>", methods=["GET"])
def get_all_type(type):
    """ Returns properties in the the portfolio based off the type """
    try:
        all_type = property_manager.get_property_details(type)

        response = app.response_class(
            status=200,
            response=json.dumps(all_type),
            mimetype='application/json'
        )
        return response

    except ValueError as e:
        response = app.response_class(
            status=400,
            response="Invalid Property Type"
        )
        return response


@app.route("/portfolio/properties/sold", methods=["PUT"])
def sold():
    """ Get the property and mark is as sold """
    content = request.json
    try:
        parcel_number = content["parcel_number"]
        selling_price = content["selling_price"]

        property_manager.update_property(parcel_number, selling_price)

        if property_manager:
            response = app.response_class(
                status=200
            )
        else:
            response = app.response_class(
                status=404, response="Property cannot be found"
            )

    except ValueError:
        response = app.response_class(
            status=400, response="Invalid Parcel Number")
    return response


if __name__ == "__main__":
    app.run()
