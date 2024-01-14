#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestCustomReviewInstantiation
    TestCustomReviewSave
    TestCustomReviewToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestCustomReviewInstantiation(unittest.TestCase):
    """Customized unittests for testing instantiation of the Review class."""

    def test_instance_creation(self):
        self.assertEqual(Review, type(Review()))

    def test_instance_in_storage(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_custom_id_type(self):
        self.assertEqual(str, type(Review().id))

    def test_custom_created_at_type(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_custom_updated_at_type(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_custom_place_id_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rv))
        self.assertNotIn("place_id", rv.__dict__)

    def test_custom_user_id_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rv))
        self.assertNotIn("user_id", rv.__dict__)

    def test_custom_text_attribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rv))
        self.assertNotIn("text", rv.__dict__)

    def test_unique_ids_for_reviews(self):
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def test_different_creation_times(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def test_different_update_times(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def test_custom_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        rv_str = rv.__str__()
        self.assertIn("[CustomReview] (123456)", rv_str)
        self.assertIn("'id': '123456'", rv_str)
        self.assertIn("'created_at': " + dt_repr, rv_str)
        self.assertIn("'updated_at': " + dt_repr, rv_str)

    def test_unused_args(self):
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def test_instantiation_with_custom_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(rv.id, "345")
        self.assertEqual(rv.created_at, dt)
        self.assertEqual(rv.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestCustomReviewSave(unittest.TestCase):
    """Customized unittests for testing save method of the Review class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("custom_file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("custom_file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "custom_file.json")
        except IOError:
            pass

    def test_single_save_operation(self):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)

    def test_double_save_operations(self):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        second_updated_at = rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rv.save()
        self.assertLess(second_updated_at, rv.updated_at)

    def test_save_with_invalid_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)

    def test_save_updates_custom_file(self):
        rv = Review()
        rv.save()
        rvid = "CustomReview." + rv.id
        with open("custom_file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestCustomReviewToDict(unittest.TestCase):
    """Customized unittests for testing to_dict method of the Review class."""

    def test_custom_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_custom_to_dict_contains_keys(self):
        rv = Review()
        self.assertIn("id", rv.to_dict())
        self.assertIn("created_at", rv.to_dict())
        self.assertIn("updated_at", rv.to_dict())
        self.assertIn("__class__", rv.to_dict())

    def test_custom_to_dict_contains_extra_attributes(self):
        rv = Review()
        rv.extra_attribute = "ExtraInfo"
        rv.custom_number = 42
        self.assertEqual("ExtraInfo", rv.extra_attribute)
        self.assertIn("custom_number", rv.to_dict())

    def test_to_dict_datetime_attributes_as_str(self):
        rv = Review()
        rv_dict = rv.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def test_custom_to_dict_output(self):
        dt = datetime.today()
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'CustomReview',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(rv.to_dict(), tdict)

    def test_compare_to_dict_with_dunder_dict(self):
        rv = Review()
        self.assertNotEqual(rv.to_dict(), rv.__dict__)

    def test_to_dict_with_invalid_arg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
