####
# Modifications copyright 2023 burrizza
# Copyright 2014 Mateusz Harasymczuk, Gonchik Tsymzhitov (atlassian-api)
######
import logging

from .rest_client import FedRepRestAPI

logger = logging.getLogger(__name__)

class NinaAPI(FedRepRestAPI):
    """
    Nina Constructor using FedRepRestAPI as base
    (mostly copied from atlassian-python-api see NOTICE)
    API Documentation: https://nina.api.bund.dev/
    """

    def __init__(self, url, *args, **kwargs):
        if 'api_version' not in kwargs:
            kwargs['api_version'] = 'api31'
        if 'api_root' not in kwargs:
            kwargs['api_root'] = None
        super(NinaAPI, self).__init__(url, *args, **kwargs)

    def mowas_warnings(self, expand=None):
        """
        Retrieve MOdular WArn System (for the citizens of Germany) warnings using the NINA interface.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='mowas')
        url = f'{base_url}/mapData.json'
        params = {}
        if expand:
            params['expand'] = expand
        return self.get(url, params=params)

    def katwarn_warnings(self, expand=None):
        """
        Retrieve KAT_wARN (Katastrophenschutz - civil protection warn system Germany) warnings using the NINA interface.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='katwarn')
        url = f'{base_url}/mapData.json'
        params = {}
        if expand:
            params['expand'] = expand
        return self.get(url, params=params)

    def dwd_warnings(self, expand=None):
        """
        Retrieve D_wD (german weather service) warnings using the NINA interface.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='dwd')
        url = f'{base_url}/mapData.json'
        params = {}
        if expand:
            params['expand'] = expand  # TODO: expand is jira specific, eg "&expand=None"
        return self.get(url, params=params)

    def biwapp_warnings(self, expand=None):
        """
        Retrieve BIWapp (Buerger Info und Warnapp - german citizen warn application) warnings using the NINA interface.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='biwapp')
        url = f'{base_url}/mapData.json'
        params = {}
        if expand:
            params['expand'] = expand  # TODO: expand is jira specific, eg "&expand=None"
        return self.get(url, params=params)

    def police_warnings(self, expand=None):
        """
        Retrieve police warnings using the NINA interface.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='police')
        url = f'{base_url}/mapData.json'
        params = {}
        if expand:
            params['expand'] = expand  # TODO: expand is jira specific, eg "&expand=None"
        return self.get(url, params=params)

    def lhp_warnings(self, expand=None):
        """
        Retrieve lhp (Hochwasser Portal - german flood warning system) warnings using the NINA interface.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='lhp')
        url = f'{base_url}/mapData.json'
        params = {}
        if expand:
            params['expand'] = expand  # TODO: expand is jira specific, eg "&expand=None"
        return self.get(url, params=params)

    def warning_detail(self, key, expand=None):
        """
        Delivers additional information about a warning.
        Args:
            key: The Id corresponding to the warning of interest.
            expand: Out of Order (TODO)

        Returns: Dict with additional informations to a warning.
        """
        base_url = self.resource_url(resource='warnings')
        url = f'{base_url}/{key}.json'
        params = {}
        if expand:
            params['expand'] = expand
        return self.get(url, params=params)

    def warning_geo(self, key, expand=None):
        """
        Delivers geographical information about a warning.
        Args:
            key: The Id corresponding to the warning of interest.
            expand: Out of Order (TODO)

        Returns: Dict with geographical informations to a warning.
        """
        base_url = self.resource_url(resource='warnings')
        url = f'{base_url}/{key}.geojson'
        params = {}
        if expand:
            params['expand'] = expand
        return self.get(url, params=params)

    def generic_complete(self, resp_warnings, selection=None, expand=None):
        """
        Delivers all List with all information to the given warnings.
        Args:
            resp_warnings: A list with the response of the warnings which should be completed.
            selection: A list with a selection of the toplevel fields of interest.
            expand: Out of Order (TODO)

        Returns: A List with all available informations to given warnings.
        """
        genericCompList = list()
        for resp in resp_warnings:
            resp_id = resp.get('id')
            if (selection is None):
                genericCompEntry = {'warning': resp, 'warning_detail': self.warning_detail(key=resp_id),
                                    'warning_geo': self.warning_geo(key=resp_id)}
            else:
                respDetail = self.warning_detail(key=resp_id)
                respGeo = self.warning_geo(key=resp_id)
                genericCompEntry = {
                    'warning': {key: resp[key] for key in resp.keys() if key in selection},
                    'warning_detail': {key: respDetail[key] for key in respDetail.keys() if key in selection},
                    'warning_geo': {key: respGeo.get(key) for key in respGeo.keys() if key in selection}
                }
            genericCompList.append(genericCompEntry)
        return genericCompList

    JSON_SCHEMA_DWD_WARNINGS = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'version': {'type': 'number'},
                'urgency': {'type': 'string'},
                'startDate': {'type': 'string'},
                'expiresDate': {'type': 'string'},
                'severity': {'type': 'string'},
                'type': {'type': 'string'},
                'i18nTitle': {'type': 'object'},
            },
            'required': ['id', 'version', 'startDate', 'expiresDate', 'severity', 'type', 'i18nTitle'],
            'additionalProperties': False
        }
    }

    JSON_SCHEMA_KATWARN_WARNINGS = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'version': {'type': 'number'},
                'urgency': {'type': 'string'},
                'startDate': {'type': 'string'},
                'expiresDate': {'type': 'string'},
                'severity': {'type': 'string'},
                'type': {'type': 'string'},
                'i18nTitle': {'type': 'object'},
                'transKeys': {'type': 'object'},
            },
            'required': ['id', 'version', 'startDate', 'severity', 'type', 'i18nTitle'],
            'additionalProperties': False
        }
    }

    JSON_SCHEMA_MOWAS_WARNINGS = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'version': {'type': 'number'},
                'urgency': {'type': 'string'},
                'startDate': {'type': 'string'},
                'expiresDate': {'type': 'string'},
                'severity': {'type': 'string'},
                'type': {'type': 'string'},
                'i18nTitle': {'type': 'object'},
                'transKeys': {'type': 'object'},
            },
            'required': ['id', 'version', 'startDate', 'severity', 'type', 'i18nTitle', 'transKeys'],
            'additionalProperties': False
        }
    }

    JSON_SCHEMA_BIWAPP_WARNINGS = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'version': {'type': 'number'},
                'urgency': {'type': 'string'},
                'startDate': {'type': 'string'},
                'expiresDate': {'type': 'string'},
                'severity': {'type': 'string'},
                'type': {'type': 'string'},
                'i18nTitle': {'type': 'object'},
                'transKeys': {'type': 'object'},
            },
            'required': ['id', 'version', 'startDate', 'severity', 'type', 'i18nTitle'],
            'additionalProperties': False
        }
    }

    JSON_SCHEMA_POLICE_WARNINGS = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'version': {'type': 'number'},
                'urgency': {'type': 'string'},
                'startDate': {'type': 'string'},
                'expiresDate': {'type': 'string'},
                'severity': {'type': 'string'},
                'type': {'type': 'string'},
                'i18nTitle': {'type': 'object'},
                'transKeys': {'type': 'object'},
            },
            'required': ['id', 'version', 'startDate', 'severity', 'type', 'i18nTitle'],
            'additionalProperties': False
        }
    }

    JSON_SCHEMA_LHP_WARNINGS = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'version': {'type': 'number'},
                'urgency': {'type': 'string'},
                'startDate': {'type': 'string'},
                'expiresDate': {'type': 'string'},
                'severity': {'type': 'string'},
                'type': {'type': 'string'},
                'i18nTitle': {'type': 'object'},
                'transKeys': {'type': 'object'},
            },
            'required': ['id', 'version', 'startDate', 'severity', 'type', 'i18nTitle'],
            'additionalProperties': False
        }
    }

    JSON_SCHEMA_WARNINGS_DETAIL = {
        'type': 'object',
        'properties': {
            'identifier': {'type': 'string'},
            'sender': {'type': 'string'},
            'source': {'type': 'string'},
            'sent': {'type': 'string'},
            'status': {'type': 'string'},
            'msgType': {'type': 'string'},
            'scope': {'type': 'string'},
            'references': {'type': 'string'},
            'code': {'type': 'array'},
            'incidents': {'type': 'string'},
            'info': {'type': 'array'},
        },
        'required': ['identifier', 'sender', 'sent', 'status', 'msgType', 'scope', 'code', 'info'],
        'additionalProperties': False
    }

    JSON_SCHEMA_WARNINGS_GEO = {
        'type': 'object',
        'properties': {
            'type': {'type': 'string'},
            'features': {'type': 'array'},
        },
        'required': ['type', 'features'],
        'additionalProperties': False
    }

    JSON_SCHEMA_WARNINGS_COMPLETE = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'warning': {'type': 'object'},
                'warning_detail': {'type': 'object'},
                'warning_geo': {'type': 'object'},
            },
            'required': ['warning', 'warning_detail', 'warning_geo'],
            'additionalProperties': False
        }
    }
