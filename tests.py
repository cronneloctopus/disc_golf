#!/usr/bin/env python
import unittest
from config import app
from mongoengine import connect
from disc_golf.models import User


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.u = User(username='john', email='john@example.com')
        self.u.save()

    def tearDown(self):
        self.u.delete()

    def test_created_user(self):
        self.assertEqual(self.u.username, 'john')


suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
