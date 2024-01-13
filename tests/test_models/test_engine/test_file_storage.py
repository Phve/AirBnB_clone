#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorageInitialization
    TestFileStorageMethods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInitialization(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_initialization_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_initialization_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_instance(self):
        base_model = BaseModel()
        user_model = User()
        state_model = State()
        place_model = Place()
        city_model = City()
        amenity_model = Amenity()
        review_model = Review()

        models.storage.new(base_model)
        models.storage.new(user_model)
        models.storage.new(state_model)
        models.storage.new(place_model)
        models.storage.new(city_model)
        models.storage.new(amenity_model)
        models.storage.new(review_model)

        self.assertIn("BaseModel." + base_model.id, models.storage.all().keys())
        self.assertIn(base_model, models.storage.all().values())
        self.assertIn("User." + user_model.id, models.storage.all().keys())
        self.assertIn(user_model, models.storage.all().values())
        self.assertIn("State." + state_model.id, models.storage.all().keys())
        self.assertIn(state_model, models.storage.all().values())
        self.assertIn("Place." + place_model.id, models.storage.all().keys())
        self.assertIn(place_model, models.storage.all().values())
        self.assertIn("City." + city_model.id, models.storage.all().keys())
        self.assertIn(city_model, models.storage.all().values())
        self.assertIn("Amenity." + amenity_model.id, models.storage.all().keys())
        self.assertIn(amenity_model, models.storage.all().values())
        self.assertIn("Review." + review_model.id, models.storage.all().keys())
        self.assertIn(review_model, models.storage.all().values())

    def test_new_instance_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_instance_with_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        base_model = BaseModel()
        user_model = User()
        state_model = State()
        place_model = Place()
        city_model = City()
        amenity_model = Amenity()
        review_model = Review()

        models.storage.new(base_model)
        models.storage.new(user_model)
        models.storage.new(state_model)
        models.storage.new(place_model)
        models.storage.new(city_model)
        models.storage.new(amenity_model)
        models.storage.new(review_model)

        models.storage.save()

        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + base_model.id, save_text)
            self.assertIn("User." + user_model.id, save_text)
            self.assertIn("State." + state_model.id, save_text)
            self.assertIn("Place." + place_model.id, save_text)
            self.assertIn("City." + city_model.id, save_text)
            self.assertIn("Amenity." + amenity_model.id, save_text)
            self.assertIn("Review." + review_model.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        base_model = BaseModel()
        user_model = User()
        state_model = State()
        place_model = Place()
        city_model = City()
        amenity_model = Amenity()
        review_model = Review()

        models.storage.new(base_model)
        models.storage.new(user_model)
        models.storage.new(state_model)
        models.storage.new(place_model)
        models.storage.new(city_model)
        models.storage.new(amenity_model)
        models.storage.new(review_model)

        models.storage.save()
        models.storage.reload()

        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + base_model.id, objs)
        self.assertIn("User." + user_model.id, objs)
        self.assertIn("State." + state_model.id, objs)
        self.assertIn("Place." + place_model.id, objs)
        self.assertIn("City." + city_model.id, objs)
        self.assertIn("Amenity." + amenity_model.id, objs)
        self.assertIn("Review." + review_model.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()

