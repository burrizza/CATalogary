####
# Modifications copyright 2023 burrizza
# Copyright 2014 Mateusz Harasymczuk, Gonchik Tsymzhitov (atlassian-api)
######
import json
import logging
import sys
import unittest
from datetime import datetime, date, timedelta
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
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(sys.stdout)) # thanks to Fabio Zadrozny (
                                                             # https://stackoverflow.com/a/7483862)
        self.umbamt = UmweltbundesamtAPI(url=f'https://umweltbundesamt.api.proxy.bund.dev/api/air_data/')

    def test_get_stationsAll(self):
        """Retrieve all oxygen measurement stations from Umweltbundesamt interface."""
        resp = self.umbamt.stations()
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_STATIONS)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    def test_get_stationsCurrent(self):
        """Retrieve metadata including the measurement stations from Umweltbundesamt interface."""
        yesterday = date.today() - timedelta(days=1)
        resp = self.umbamt.meta(date_from=yesterday.strftime("%Y-%m-%d"))

        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_META)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    def test_get_components(self):
        """Retrieve all components from Umweltbundesamt interface if exists."""
        resp = self.umbamt.components()
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_COMPONENTS)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    def test_get_measures(self):
        """Retrieve all measurements from Umweltbundesamt interface if exist."""
        yesterday = date.today() - timedelta(days=1)
        resp = self.umbamt.measures(date_from=yesterday.strftime("%Y-%m-%d"))
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            validate(instance=resp, schema=self.umbamt.JSON_SCHEMA_UMWELTBAMT_MEASURES)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    def test_get_measuresAllComp(self):
        """Retrieve measurements from all components dynamically."""
        yesterday = date.today() - timedelta(days=1)
        resp_comp = self.umbamt.components()

        resp = self.umbamt.measures_components(respComponents=resp_comp, date_from=yesterday.strftime("%Y-%m-%d"))
        self.assertIsInstance(resp, dict)
        if (len(resp)):
            self.assertIsInstance(resp, dict)
            logger.debug(json.dumps(resp.get('21'), ensure_ascii=False))

    def test_get_measuresAll(self):
        """Should cover the default use cases including stations and hourly bases measurements."""
        yesterday = date.today() - timedelta(days=1)
        resp_comp = self.umbamt.components()


        resp = self.umbamt.measures_stations(respComponents=resp_comp,
                                             time_from=(datetime.utcnow() + timedelta(hours=1) # utcnow +1 is used
                                                        - timedelta(hours=1)).strftime('%H'),  # -1h frequency
                                             date_from=date.today().strftime("%Y-%m-%d"),
                                             dict_scopes = {'1': '1TMW', '2': '1SMW', '3': '1SMW_MAX', '6': '1TMWGL'})
        self.assertIsInstance(resp_comp, dict)
        if (len(resp)):
            self.assertIsInstance(resp, list)
            logger.debug(json.dumps(resp[:20], ensure_ascii=False))

if __name__ == '__main__':
    unittest.main()
