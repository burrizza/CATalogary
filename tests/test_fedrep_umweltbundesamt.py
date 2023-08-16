####
# Modifications copyright 2023 burrizza
# Copyright 2014 Mateusz Harasymczuk, Gonchik Tsymzhitov (atlassian-api)
######
import logging
import sys
import unittest
from datetime import date, timedelta
from unittest import TestCase

from jsonschema import validate

from catalogary import UmweltbundesamtAPI

logger = logging.getLogger()

class TestUmweltbundesamt(TestCase):
    """
    Tests for the Umweltbundesamt API
    (mostly copied from atlassian-python-api see NOTICE)
    """

    def setUp(self):
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout)) # thanks to Fabio Zadrozny (
                                                             # https://stackoverflow.com/a/7483862)
        self.umbamt = UmweltbundesamtAPI(url=f'https://umweltbundesamt.api.proxy.bund.dev/api/air_data/')

    def test_get_stationsAll(self):
        """Retrieve oxygen measurement stations from Umweltbundesamt interface if exist"""
        resp = self.umbamt.stations()
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_STATIONS)

    def test_get_stationsCurrent(self):
        """Retrieve oxygen measurement stations from Umweltbundesamt interface if exist"""
        yesterday = date.today() - timedelta(days=1)
        resp = self.umbamt.meta(date_from=yesterday.strftime("%Y-%m-%d"))

        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_META)

    def test_get_components(self):
        """Retrieve all measures from Umweltbundesamt interface if exist"""
        resp = self.umbamt.components()
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_COMPONENTS)

    def test_get_measures(self):
        """Retrieve all measures from Umweltbundesamt interface if exist"""
        yesterday = date.today() - timedelta(days=1)
        resp = self.umbamt.measures(date_from=yesterday.strftime("%Y-%m-%d"))
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_MEASURES)

    def test_get_measuresAllComp(self):
        """Retrieve all measures from Umweltbundesamt interface if exist"""
        yesterday = date.today() - timedelta(days=1)
        resp_comp = self.umbamt.components()

        resp = self.umbamt.measures_components(respComponents=resp_comp, date_from=yesterday.strftime("%Y-%m-%d"))
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            self.assertIsInstance(resp, dict)
            # print('Umweltbamt measures yesterday all components')
            # print(json.dumps(resp.get('21')))


if __name__ == '__main__':
    unittest.main()
