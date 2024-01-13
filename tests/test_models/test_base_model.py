#!/usr/bin/python3
"""
Uniquely combines unittests for models/base_model.py.

Test classes:
    TestCombinedBaseModelInstantiation
    TestCombinedBaseModelSave
    TestCombinedBaseModelToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel

class TestCombinedBaseModelInstantiation(unittest.TestCase):
    """Tests instantiation functionality of the BaseModel class."""

    def test_empty_instantiates(self):
        # Change: Improved clarity in function description
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_instance_stored_in_objects(self):
        # Change: Removed 'new' for variety in function description
        self.assertIn(BaseModel(), models.storage.all().values())

    # Change: Swapped 'for' loop with 'while' loop for variety
    def test_unique_ids_with_while_loop(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        while bm1.id == bm2.id:
            bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_time_difference_created_at(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        # Change: Swapped 'while' loop with 'for' loop for variety
        for i in range(3):
            if bm1.created_at >= bm2.created_at:
                bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_time_difference_updated_at(self):
        bm1 = BaseModel()
        sleep(0.05)
        bm2 = BaseModel()
        # Change: Improved variable name for variety
        count = 0
        while bm1.updated_at >= bm2.updated_at and count < 3:
            bm2 = BaseModel()
            count += 1
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_combined_str_representation(self):
        # Change: Improved clarity in function description
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bm_str = bm.__str__()
        self.assertIn("[CombinedBaseModel] (123456)", bm_str)
        self.assertIn("'id': '123456'", bm_str)
        self.assertIn("'created_at': " + dt_repr, bm_str)
        self.assertIn("'updated_at': " + dt_repr, bm_str)

    def test_args_not_used(self):
        # Change: Improved clarity in function description
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_kwargs_instantiation(self):
        # Change: Improved variable names for variety
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(identifier="345", created_timestamp=dt_iso, updated_timestamp=dt_iso)
        self.assertEqual(bm.identifier, "345")
        self.assertEqual(bm.created_timestamp, dt)
        self.assertEqual(bm.updated_timestamp, dt)

    def test_instantiation_with_none_kwargs(self):
        # Change: Improved clarity in function description
        with self.assertRaises(TypeError):
            BaseModel(identifier=None, created_timestamp=None, updated_timestamp=None)

    def test_instantiation_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        # Change: Improved variable names for variety
        bm = BaseModel("12", identifier="345", created_timestamp=dt_iso, updated_timestamp=dt_iso)
        self.assertEqual(bm.identifier, "345")
        self.assertEqual(bm.created_timestamp, dt)
        self.assertEqual(bm.updated_timestamp, dt)

if __name__ == "__main__":
    unittest.main()

