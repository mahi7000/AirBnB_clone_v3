#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def setUp(self):
        """Set up test environment"""
        self.storage = DBStorage()
        self.storage.reload()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_object = {"name": "Lagos"}
        new_state = State(**state_object)
        self.storage.new(new_state)
        self.storage.save()

        all_stored_object = self.storage.all()
        self.assertTrue(len(all_stored_object) > 0)
        self.assertIn(new_state.id, all_stored_object)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        """Test that new adds an object to the database"""
        state_object = {"name": "Ontario"}
        new_object = State(**state_object)

        self.storage.new(new_object)
        self.storage.save()

        all_objects = self.storage.all()
        retrieved_object = all_objects[new_object.id]
        self.assertIn(new_object.id, all_objects)
        self.assertEqual(retrieved_object.name, state_object["name"])
        self.assertIsNotNone(retrieved_object)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_object = {"name": "Newyork"}
        new_object = State(**state_object)

        self.storage.new(new_object)
        self.storage.save()

        all_objects = self.storage.all()
        retrieved_object = all_objects[new_object.id]
        self.assertIn(new_object.id, all_objects)
        self.assertEqual(retrieved_object.name, state_object["name"])
        self.assertIsNotNone(retrieved_object)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test method for obtaining an instance of db storage"""
        storage = models.DBStorage()
        storage.reload()

        state_object = {"name": "New Mexico"}
        new_object = State(**state_object)

        storage.new(new_object)
        storage.save()

        retrieved_object = storage.get(State, new_object.id)
        self.assertEqual(new_object.name, retrieved_object.name)

        fake_object = storage.get(State, 'fake_id')
        self.assertIsNone(fake_object)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test method for obtaining an instance of db storage"""
        storage = models.DBStorage()
        storage.reload()

        state_object = {"name": "Paris"}
        new_state = State(**state_object)
        storage.new(new_state)
        storage.save()

        city_object = {"name": "Panama"}
        new_city = City(**city_object)
        storage.new(new_city)
        storage.save()

        s_occurrence = storage.count(State)
        self.assertEqual(s_occurrence, len(storage.all(State)))

        all_occurrence = storage.count()
        self.assertEqual(all_occurrence, len(storage.all()))
