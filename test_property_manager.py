import unittest
from property_manager import PropertyManager
from unittest import TestCase
import inspect
from condo import Condo
from duplex import Duplex

from sqlalchemy import create_engine
from base import Base
import os


class TestPropertyManager(TestCase):
    """ Tests for the PropertyManager class """

    def setUp(self):
        engine = create_engine('sqlite:///test_properties.sqlite')

        # Creates all the tables
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        self.properties_mgr = PropertyManager("Andrew's Portfolio",
                                              'test_properties.sqlite')
        self.logPoint()
        self._test_condo = Condo(
            "1234", "Buckingham", "Burnaby", "V6LV8S", 50.0, 89, "Concord", 200)
        self._test_duplex = Duplex(
            "5678", "Heights", "Vancouver", "V9LV0S", 50.0, 89, 20, 200)

    def tearDown(self):
        os.remove('test_properties.sqlite')
        self.logPoint()

    def logPoint(self):
        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

    def test_init_success(self):
        """ 010A - Successfully creates a PropertyManager object """

        self.assertIsInstance(self.properties_mgr, PropertyManager)

    def test_get_portfolio_name(self):
        """ 020A - Verify get all properties """

        self.assertEqual(
            (self.properties_mgr.get_portfolio_name()), "Andrew's Portfolio"
        )

    def test_property_exists_success(self):
        """ 030A - Returns the expected details when a property exists """
        self.properties_mgr.add_property(self._test_condo)
        self.assertTrue(self.properties_mgr.property_exists('1234'))

        self.properties_mgr.add_property(self._test_duplex)
        self.assertTrue(self.properties_mgr.property_exists('5678'))

    def test_property_exists_failure(self):
        """ 030B - Returns the expected details when a property doesnt exists """
        self.assertRaisesRegex(ValueError,
                               "Invalid Parcel Number.",
                               self.properties_mgr.property_exists, None)

    def test_add_property_success(self):
        """ 040A - Successfully add a property """

        self.properties_mgr.add_property(self._test_condo)
        self.properties_mgr.add_property(self._test_duplex)

        self.assertFalse(
            self.properties_mgr.get_property_by_parcel_num('1235'))
        self.assertIsNotNone(
            self.properties_mgr.get_property_by_parcel_num('1234'))

        self.assertFalse(
            self.properties_mgr.get_property_by_parcel_num('5679'))
        self.assertIsNotNone(
            self.properties_mgr.get_property_by_parcel_num('5678'))

    def test_add_property_errors(self):
        """ 040B - Verify invalid property results in an exception """

        self.assertRaisesRegex(
            ValueError, "Invalid Property.", self.properties_mgr.add_property, None)

    def test_get_property_by_parcel_num_success(self):
        """ 050A - Verify that you can get a property by the parcel number """

        self.properties_mgr.add_property(self._test_condo)
        self.assertIsNotNone(
            self.properties_mgr.get_property_by_parcel_num('1234'))

        self.properties_mgr.add_property(self._test_duplex)
        self.assertIsNotNone(
            self.properties_mgr.get_property_by_parcel_num('5678'))

    def test_get_property_by_parcel_num_return_none(self):
        """ 050B - Verify that if the property number doesnt exist, returns None """
        self.assertIs(
            self.properties_mgr.get_property_by_parcel_num('1234'), None)

    def test_get_property_by_parcel_num_failure(self):
        """ 050C - Verify that invalid property parcel number results in an exception """
        self.assertRaisesRegex(
            ValueError, "Invalid Parcel Number.",
            self.properties_mgr.get_property_by_parcel_num, None)

    def test_update_property_success(self):
        self.properties_mgr.add_property(self._test_condo)

        self.properties_mgr.update_property("1234", 110.2)

        test_condo = self.properties_mgr.get_property_by_parcel_num("1234")
        self.assertTrue(
            test_condo.is_sold)

    def test_delete_property_by_parcel_num_success(self):
        """ 060A - Delete property by parcel number success """

        self.properties_mgr.add_property(self._test_condo)

        self.assertEqual(
            len(self.properties_mgr.get_property_details("Condo")), 1
        )

        self.properties_mgr.delete_property_by_parcel_num('1234')

        self.assertEqual(
            len(self.properties_mgr.get_property_details("Condo")), 0
        )

        self.properties_mgr.add_property(self._test_duplex)

        self.assertEqual(
            len(self.properties_mgr.get_property_details("Duplex")), 1
        )

        self.properties_mgr.delete_property_by_parcel_num('5678')

        self.assertEqual(
            len(self.properties_mgr.get_property_details("Duplex")), 0
        )

    def test_delete_property_by_parcel_num_ignore(self):
        """ 060B - Delete property by parcel number. If the parcel number dosnt exist, ignore. """

        self.assertRaisesRegex(
            ValueError, "Invalid Parcel Number.",
            self.properties_mgr.delete_property_by_parcel_num, 1234)

    def test_delete_property_by_parcel_num_errors(self):
        """ 060C - Delete property by parcel number. Error if the parcel number is not defined """
        self.assertRaisesRegex(
            ValueError, "Invalid Parcel Number.",
            self.properties_mgr.delete_property_by_parcel_num, None)


if __name__ == "__main__":
    unittest.main()
