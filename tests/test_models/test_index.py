#!/usr/bin/python3
""" Test for Index.py file """

import unittest
from unittest.mock import patch
from io import StringIO
import json
from api.v1.app import app
from api.v1.views import app_views
from models import storage

class TestIndexdoc(unittest.TestCase):
    """ Class to test the Index.py file """

    def test_indexdoc(self):
        """ Test the documentation """
        self.assertIsNotNone(("api/v1/views/index.py".__doc__))
        self.assertIsNotNone(app_views.__doc__)
        self.assertIsNotNone(app_views.index.__doc__)

    def test_index(self):
        """ Test the index method """
        with app.test_client() as client:
            response = client.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {'status': 'OK'})

class TestStats(unittest.TestCase):
    """ Test the stats method """

    def test_stats(self):
        """ Test the stats method """
        with app.test_client() as client:
            response = client.get('/api/v1/stats')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {'amenities': 0, 'cities': 0, 'places': 0, 'reviews': 0, 'states': 0, 'users': 0})

    def test_stats2(self):
        """ Test the stats method """
        with app.test_client() as client:
            response = client.get('/api/v1/stats/amenities')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {'amenities': 0})
            