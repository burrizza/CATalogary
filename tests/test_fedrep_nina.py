####
# Modifications copyright 2023 burrizza
# Copyright 2014 Mateusz Harasymczuk, Gonchik Tsymzhitov (atlassian-api)
######
import json
import logging
import sys
import unittest
from unittest import TestCase

from jsonschema import validate

from catalogary import NinaAPI

logger = logging.getLogger()

class TestNina(TestCase):
    """
    Tests for the Nina API
    (mostly copied from atlassian-python-api see NOTICE)
    """

    def setUp(self):
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(sys.stdout)) # thanks to Fabio Zadrozny (
                                                             # https://stackoverflow.com/a/7483862)
        self.nina = NinaAPI(url=f'https://nina.api.proxy.bund.dev/')

    # KAT_warn
    def test_get_katwarn_warnings(self):
        """Retrieve KAT_wARN warnings from NINA interface if exist"""
        resp = self.nina.katwarn_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_KATWARN_WARNINGS)

    def test_get_katwarn_warning_detail(self):
        """Retrieve KAT_wARN warnings from NINA interface if exist"""
        resp = self.nina.katwarn_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_detail = self.nina.warning_detail(key=resp_id)
            validate(instance=resp_detail, schema=self.nina.JSON_SCHEMA_WARNINGS_DETAIL)

    def test_get_katwarn_warning_geo(self):
        """Retrieve KAT_wARN warnings from NINA interface if exist"""
        resp = self.nina.katwarn_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_geo = self.nina.warning_geo(key=resp_id)
            validate(instance=resp_geo, schema=self.nina.JSON_SCHEMA_WARNINGS_GEO)

    def test_get_katwarnComplete(self):
        """Retrieve KAT_wARN warnings from NINA interface if exist"""
        resp_warnings = self.nina.katwarn_warnings()
        resp = self.nina.generic_complete(resp_warnings, selection=['id',
                                                                    'startDate',
                                                                    'expiresDate',
                                                                    'severity',
                                                                    'i18nTitle',
                                                                    'info',
                                                                    'sent',
                                                                    'features'])
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_WARNINGS_COMPLETE)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    # Mo_waS
    def test_get_mowas_warnings(self):
        """Retrieve Mo_waS warnings from NINA interface if exist"""
        resp = self.nina.mowas_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_MOWAS_WARNINGS)

    def test_get_mowa_warning_detail(self):
        """Retrieve Mo_waS warnings from NINA interface if exist"""
        resp = self.nina.mowas_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_detail = self.nina.warning_detail(key=resp_id)
            validate(instance=resp_detail, schema=self.nina.JSON_SCHEMA_WARNINGS_DETAIL)

    def test_get_mowa_warning_geo(self):
        """Retrieve Mo_waS warnings from NINA interface if exist"""
        resp = self.nina.mowas_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_geo = self.nina.warning_geo(key=resp_id)
            validate(instance=resp_geo, schema=self.nina.JSON_SCHEMA_WARNINGS_GEO)

    def test_get_mowasComplete(self):
        """Retrieve Mo_waS warnings from NINA interface if exist"""
        resp_warnings = self.nina.mowas_warnings()
        resp = self.nina.generic_complete(resp_warnings, selection=['id',
                                                                    'startDate',
                                                                    'expiresDate',
                                                                    'severity',
                                                                    'i18nTitle',
                                                                    'info',
                                                                    'sent',
                                                                    'features'])
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_WARNINGS_COMPLETE)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    # D_wD
    def test_get_dwd_warnings(self):
        """Retrieve D_wD warnings from NINA interface if exist"""
        resp = self.nina.dwd_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_DWD_WARNINGS)

    def test_get_dwd_warning_detail(self):
        """Retrieve D_wD warnings from NINA interface if exist"""
        resp = self.nina.dwd_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_detail = self.nina.warning_detail(key=resp_id)
            validate(instance=resp_detail, schema=self.nina.JSON_SCHEMA_WARNINGS_DETAIL)

    def test_get_dwd_warning_geo(self):
        """Retrieve D_wD warnings from NINA interface if exist"""
        resp = self.nina.dwd_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_geo = self.nina.warning_geo(key=resp_id)
            validate(instance=resp_geo, schema=self.nina.JSON_SCHEMA_WARNINGS_GEO)

    def test_get_dwdComplete(self):
        """Retrieve D_wD warnings from NINA interface if exist"""
        resp_warnings = self.nina.dwd_warnings()
        resp = self.nina.generic_complete(resp_warnings, selection=['id',
                                                                    'startDate',
                                                                    'expiresDate',
                                                                    'severity',
                                                                    'i18nTitle',
                                                                    'info',
                                                                    'sent',
                                                                    'features'])
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_WARNINGS_COMPLETE)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    # _wIAPP
    def test_get_biwapp_warnings(self):
        """Retrieve BI_wAPP warnings from NINA interface if exist"""
        resp = self.nina.biwapp_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_BIWAPP_WARNINGS)

    def test_get_biwapp_warning_detail(self):
        """Retrieve BI_wAPP warnings from NINA interface if exist"""
        resp = self.nina.biwapp_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_detail = self.nina.warning_detail(key=resp_id)
            validate(instance=resp_detail, schema=self.nina.JSON_SCHEMA_WARNINGS_DETAIL)

    def test_get_biwapp_warning_geo(self):
        """Retrieve BI_wAPP warnings from NINA interface if exist"""
        resp = self.nina.biwapp_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_geo = self.nina.warning_geo(key=resp_id)
            validate(instance=resp_geo, schema=self.nina.JSON_SCHEMA_WARNINGS_GEO)

    def test_get_biwappComplete(self):
        """Retrieve BI_wAPP warnings from NINA interface if exist"""
        resp_warnings = self.nina.biwapp_warnings()
        resp = self.nina.generic_complete(resp_warnings, selection=['id',
                                                                    'startDate',
                                                                    'expiresDate',
                                                                    'severity',
                                                                    'i18nTitle',
                                                                    'info',
                                                                    'sent',
                                                                    'features'])
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_WARNINGS_COMPLETE)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    # Police
    def test_get_police_warnings(self):
        """Retrieve police warnings from NINA interface if exist"""
        resp = self.nina.police_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_POLICE_WARNINGS)

    def test_get_police_warning_detail(self):
        """Retrieve police warnings from NINA interface if exist"""
        resp = self.nina.police_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_detail = self.nina.warning_detail(key=resp_id)
            validate(instance=resp_detail, schema=self.nina.JSON_SCHEMA_WARNINGS_DETAIL)

    def test_get_police_warning_geo(self):
        """Retrieve police warnings from NINA interface if exist"""
        resp = self.nina.police_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_geo = self.nina.warning_geo(key=resp_id)
            validate(instance=resp_geo, schema=self.nina.JSON_SCHEMA_WARNINGS_GEO)

    def test_get_policeComplete(self):
        """Retrieve police warnings from NINA interface if exist"""
        resp_warnings = self.nina.police_warnings()
        resp = self.nina.generic_complete(resp_warnings, selection=['id',
                                                                    'startDate',
                                                                    'expiresDate',
                                                                    'severity',
                                                                    'i18nTitle',
                                                                    'info',
                                                                    'sent',
                                                                    'features'])
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_WARNINGS_COMPLETE)
            logger.debug(json.dumps(resp, ensure_ascii=False))

    # Lhp - High Tide warnings
    def test_get_lhpMapData(self):
        """Retrieve LHP warnings from NINA interface if exist"""
        resp = self.nina.lhd_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_LHP_WARNINGS)

    def test_get_lhp_warning_detail(self):
        """Retrieve LHP warnings from NINA interface if exist"""
        resp = self.nina.lhd_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_detail = self.nina.warning_detail(key=resp_id)
            validate(instance=resp_detail, schema=self.nina.JSON_SCHEMA_WARNINGS_DETAIL)

    def test_get_lhp_warning_geo(self):
        """Retrieve LHP warnings from NINA interface if exist"""
        resp = self.nina.lhd_warnings()
        self.assertIsInstance(resp, list)
        if len(resp):
            resp_id = resp[0]['id']
            resp_geo = self.nina.warning_geo(key=resp_id)
            validate(instance=resp_geo, schema=self.nina.JSON_SCHEMA_WARNINGS_GEO)

    def test_get_lhpComplete(self):
        """Retrieve LHP warnings from NINA interface if exist"""
        resp_warnings = self.nina.lhd_warnings()
        resp = self.nina.generic_complete(resp_warnings, selection=['id',
                                                                    'startDate',
                                                                    'expiresDate',
                                                                    'severity',
                                                                    'i18nTitle',
                                                                    'info',
                                                                    'sent',
                                                                    'features'])
        self.assertIsInstance(resp, list)
        if len(resp):
            validate(instance=resp, schema=self.nina.JSON_SCHEMA_WARNINGS_COMPLETE)
            logger.debug(json.dumps(resp, ensure_ascii=False))

if __name__ == '__main__':
    unittest.main()
