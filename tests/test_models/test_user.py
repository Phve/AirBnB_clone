#!/usr/bin/python3
"""Custom unittests for models/user.py.

Custom Unittest classes:
    CustomUserInstantiationTest
    CustomUserSaveTest
    CustomUserToDictTest
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class CustomUserInstantiationTest(unittest.TestCase):
    """Custom tests for instantiating the User class."""

    def test_custom_creation_without_args(self):
        self.assertEqual(User, type(User()))

    def test_custom_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_custom_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_custom_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_custom_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_custom_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_custom_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_custom_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_custom_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_custom_unique_ids_for_two_users(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_custom_different_created_at_for_two_users(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_custom_different_updated_at_for_two_users(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_custom_string_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        user_str = user.__str__()
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + dt_repr, user_str)
        self.assertIn("'updated_at': " + dt_repr, user_str)

    def test_custom_args_not_used(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_custom_instantiation_with_custom_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_custom_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class CustomUserSaveTest(unittest.TestCase):
    """Custom tests for the save method of the User class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("custom_data.json", "backup_custom_data")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("custom_data.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("backup_custom_data", "custom_data.json")
        except FileNotFoundError:
            pass

    def test_custom_single_save_operation(self):
        user_instance = User()
        sleep(0.05)
        first_updated_at = user_instance.updated_at
        user_instance.save()
        self.assertLess(first_updated_at, user_instance.updated_at)

    def test_custom_two_saves(self):
        user_instance = User()
        sleep(0.05)
        first_updated_at = user_instance.updated_at
        user_instance.save()
        second_updated_at = user_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user_instance.save()
        self.assertLess(second_updated_at, user_instance.updated_at)

    def test_custom_save_with_argument(self):
        user_instance = User()
        with self.assertRaises(TypeError):
            user_instance.save(None)

    def test_custom_save_updates_custom_data_file(self):
        user_instance = User()
        user_instance.save()
        user_id = f"User.{user_instance.id}"
        with open("custom_data.json", "r") as custom_data_file:
            self.assertIn(user_id, custom_data_file.read())


class CustomUserToDictTest(unittest.TestCase):
    """Custom tests for the to_dict method of the User class."""

    # Customize tests as needed

    def test_custom_to_dict_with_argument(self):
        user_instance = User()
        with self.assertRaises(TypeError):
            user_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

