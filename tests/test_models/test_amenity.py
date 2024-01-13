#!/usr/bin/python3
"""Defines custom unittests for models/amenity.py.

Unittest classes:
    UniqueAmenityInstantiationTests
    UniqueAmenitySaveTests
    UniqueAmenityToDictTests
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity

class UniqueAmenityInstantiationTests(unittest.TestCase):
    """Unittests for testing unique instantiation of the Amenity class."""

    def test_empty_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    # ... Additional instantiation tests ...

    def test_representation_includes_id_and_timestamps(self):
        dt_today = datetime.today()
        dt_repr = repr(dt_today)
        amenity_instance = Amenity()
        amenity_instance.id = "789012"
        amenity_instance.created_at = amenity_instance.updated_at = dt_today
        amenity_str = amenity_instance.__str__()
        self.assertIn("[UniqueAmenity] (789012)", amenity_str)
        self.assertIn("'id': '789012'", amenity_str)
        self.assertIn("'created_at': " + dt_repr, amenity_str)
        self.assertIn("'updated_at': " + dt_repr, amenity_str)

    # ... Additional instantiation tests ...

    def test_instantiation_with_kwargs(self):
        dt_today = datetime.today()
        dt_iso = dt_today.isoformat()
        amenity_instance = Amenity(id="456", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity_instance.id, "456")
        self.assertEqual(amenity_instance.created_at, dt_today)
        self.assertEqual(amenity_instance.updated_at, dt_today)

    # ... Additional instantiation tests ...

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

class UniqueAmenitySaveTests(unittest.TestCase):
    """Unittests for testing unique save method of the Amenity class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "temp_file")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp_file", "file.json")
        except IOError:
            pass

    def test_single_save_updates_timestamp(self):
        amenity_instance = Amenity()
        sleep(0.05)
        initial_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        self.assertLess(initial_updated_at, amenity_instance.updated_at)

    # ... Additional save tests ...

    def test_save_with_invalid_arg_raises_error(self):
        amenity_instance = Amenity()
        with self.assertRaises(TypeError):
            amenity_instance.save("invalid_argument")

    # ... Additional save tests ...

    def test_save_updates_json_file(self):
        amenity_instance = Amenity()
        amenity_instance.save()
        amenity_id = "UniqueAmenity." + amenity_instance.id
        with open("file.json", "r") as file:
            self.assertIn(amenity_id, file.read())

class UniqueAmenityToDictTests(unittest.TestCase):
    """Unittests for testing unique to_dict method of the Amenity class."""

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(Amenity().to_dict(), dict)

    def test_to_dict_includes_expected_keys(self):
        amenity_instance = Amenity()
        self.assertIn("id", amenity_instance.to_dict())
        self.assertIn("created_at", amenity_instance.to_dict())
        self.assertIn("updated_at", amenity_instance.to_dict())
        self.assertIn("__class__", amenity_instance.to_dict())

    # ... Additional to_dict tests ...

    def test_to_dict_datetime_attributes_are_strings(self):
        amenity_instance = Amenity()
        amenity_dict = amenity_instance.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    # ... Additional to_dict tests ...

    def test_to_dict_with_invalid_arg_raises_error(self):
        amenity_instance = Amenity()
        with self.assertRaises(TypeError):
            amenity_instance.to_dict("invalid_argument")

if __name__ == "__main__":
    unittest.main()

