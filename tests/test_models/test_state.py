#!/usr/bin/python3
"""Defines unique unittests for models/state.py.

Unittest classes:
    TestCustomStateInstantiation
    TestCustomStateSave
    TestCustomStateToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State as CustomState


class TestCustomStateInstantiation(unittest.TestCase):
    """Unit tests for checking the creation of the CustomState class."""

    def test_custom_creation_without_arguments(self):
        self.assertEqual(CustomState, type(CustomState()))

    def test_instance_stored_properly(self):
        self.assertIn(CustomState(), models.storage.all().values())

    def test_custom_id_is_str(self):
        self.assertEqual(str, type(CustomState().id))

    def test_custom_created_at_is_datetime(self):
        self.assertEqual(datetime, type(CustomState().created_at))

    def test_custom_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(CustomState().updated_at))

    def test_custom_name_is_public_class_attribute(self):
        cst = CustomState()
        self.assertEqual(str, type(CustomState.name))
        self.assertIn("name", dir(cst))
        self.assertNotIn("name", cst.__dict__)

    def test_custom_unique_ids_for_states(self):
        cst1 = CustomState()
        cst2 = CustomState()
        self.assertNotEqual(cst1.id, cst2.id)

    def test_custom_different_created_at_for_states(self):
        cst1 = CustomState()
        sleep(0.05)
        cst2 = CustomState()
        self.assertLess(cst1.created_at, cst2.created_at)

    def test_custom_different_updated_at_for_states(self):
        cst1 = CustomState()
        sleep(0.05)
        cst2 = CustomState()
        self.assertLess(cst1.updated_at, cst2.updated_at)

    def test_custom_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        cst = CustomState()
        cst.id = "123456"
        cst.created_at = cst.updated_at = dt
        cst_str = cst.__str__()
        self.assertIn("[CustomState] (123456)", cst_str)
        self.assertIn("'id': '123456'", cst_str)
        self.assertIn("'created_at': " + dt_repr, cst_str)
        self.assertIn("'updated_at': " + dt_repr, cst_str)

    def test_custom_creation_with_unused_args(self):
        cst = CustomState(None)
        self.assertNotIn(None, cst.__dict__.values())

    def test_custom_creation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cst = CustomState(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cst.id, "345")
        self.assertEqual(cst.created_at, dt)
        self.assertEqual(cst.updated_at, dt)

    def test_custom_creation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            CustomState(id=None, created_at=None, updated_at=None)


class TestCustomStateSave(unittest.TestCase):
    """Unit tests for checking the save method of the CustomState class."""

    @classmethod
    def setUp(cls):
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

    def test_custom_one_save_operation(self):
        cst = CustomState()
        sleep(0.05)
        first_updated_at = cst.updated_at
        cst.save()
        self.assertLess(first_updated_at, cst.updated_at)

    def test_custom_two_save_operations(self):
        cst = CustomState()
        sleep(0.05)
        first_updated_at = cst.updated_at
        cst.save()
        second_updated_at = cst.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cst.save()
        self.assertLess(second_updated_at, cst.updated_at)

    def test_custom_save_with_argument(self):
        cst = CustomState()
        with self.assertRaises(TypeError):
            cst.save(None)

    def test_custom_save_updates_file(self):
        cst = CustomState()
        cst.save()
        cst_id = "CustomState." + cst.id
        with open("custom_file.json", "r") as f:
            self.assertIn(cst_id, f.read())


class TestCustomStateToDict(unittest.TestCase):
    """Unit tests for checking the to_dict method of the CustomState class."""

    def test_custom_to_dict_type(self):
        self.assertTrue(dict, type(CustomState().to_dict()))

    def test_custom_to_dict_contains_correct_keys(self):
        cst = CustomState()
        self.assertIn("id", cst.to_dict())
        self.assertIn("created_at", cst.to_dict())
        self.assertIn("updated_at", cst.to_dict())
        self.assertIn("__class__", cst.to_dict())

    def test_custom_to_dict_contains_added_attributes(self):
        cst = CustomState()
        cst.middle_name = "Holberton"
        cst.my_number = 98
        self.assertEqual("Holberton", cst.middle_name)
        self.assertIn("my_number", cst.to_dict())

    def test_custom_to_dict_datetime_attributes_are_strs(self):
        cst = CustomState()
        cst_dict = cst.to_dict()
        self.assertEqual(str, type(cst_dict["id"]))
        self.assertEqual(str, type(cst_dict["created_at"]))
        self.assertEqual(str, type(cst_dict["updated_at"]))

    def test_custom_to_dict_output(self):
        dt = datetime.today()
        cst = CustomState()
        cst.id = "123456"
        cst.created_at = cst.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'CustomState',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cst.to_dict(), tdict)

    def test_custom_contrast_to_dict_dunder_dict(self):
        cst = CustomState()
        self.assertNotEqual(cst.to_dict(), cst.__dict__)

    def test_custom_to_dict_with_argument(self):
        cst = CustomState()
        with self.assertRaises(TypeError):
            cst.to_dict(None)


if __name__ == "__main__":
    unittest.main()
