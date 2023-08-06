import unittest
import gloc
from gloc import Location, Geocoordinates
import mock_data


class TestLocation(unittest.TestCase):

    def test_address_param(self):
        self.assertEqual(
            "Skånegatan%2059,%20412%2052%20Göteborg,%20Sweden",
            gloc._create_address_param("Skånegatan 59, 412 52 Göteborg, Sweden")
        )

    def test_create_address_string(self):
        self.assertEqual(
            "Skånegatan 59, 412 52 Göteborg, Sweden",
            gloc.create_address_string("Skånegatan 59", "412 52", "Göteborg", "Sweden")
        )

    def test_invalid_api_key(self):
        self.assertRaises(IOError, Location.from_address, "some_address", "an_invalid_api_key")

    def test_constructors(self):
        l1 = Location(**gloc._parse(mock_data.GÖTAPLATSEN_FROM_ADDRESS))
        l2 = Location(**gloc._parse(mock_data.GÖTAPLATSEN_FROM_COORDINATES))
        self.assertEqual(l1.street_name, l2.street_name)

    def test_city(self):
        location = Location(**gloc._parse(mock_data.DOWNING_STREET))
        self.assertEqual(location.city, "London")

    def test_distance(self):
        l1 = Location(**gloc._parse(mock_data.STOCKHOLM))
        l2 = Location(**gloc._parse(mock_data.GÖTEBORG))
        self.assertAlmostEqual(l1.distance_to(l2), 400, delta=10)

    def test_no_location(self):
        self.assertIsNone(Location(**gloc._parse(mock_data.NORTH_POLE)).country)


class TestGeocoordinates(unittest.TestCase):

    def test_distance(self):
        north_pole = Geocoordinates(90.0, 0.0)
        south_pole = Geocoordinates(-90.0, 0.0)
        self.assertAlmostEqual(north_pole.distance_to(south_pole), 20000.0, delta=100.0)

    def test_coordinate_validation(self):
        self.assertRaises(ValueError, Geocoordinates, lat=91.0, lng=180.0)


if __name__ == "__main__":
    unittest.main()
