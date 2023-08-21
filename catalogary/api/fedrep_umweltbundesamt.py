####
# Modifications copyright 2023 burrizza
# Copyright 2014 Mateusz Harasymczuk, Gonchik Tsymzhitov (atlassian-api)
######
import logging
from time import sleep

from .rest_client import FedRepRestAPI

logger = logging.getLogger(__name__)


class UmweltbundesamtAPI(FedRepRestAPI):
    """
    Umweltbumdesamt Constructor using FedRepRestAPI as base
    (mostly copied from atlassian-python-api see NOTICE)
    API Documentation: https://luftqualitaet.api.bund.dev/
    """

    def __init__(self, url, *args, **kwargs):
        if 'api_version' not in kwargs:
            kwargs['api_version'] = 'v2'
        if 'api_root' not in kwargs:
            kwargs['api_root'] = None
        super(UmweltbundesamtAPI, self).__init__(url, *args, **kwargs)

    def measures(self, date_from, time_from='24', date_to='2999-12-31', time_to='24', station=None, scope='2',
                 component='1', selection=None, expand=None):
        """
        Retrieve a component using the API of the Umweltbundesamt.
        Args:
            expand: Out of Order (TODO)

        Returns: List including the response.
        """
        base_url = self.resource_url(resource='measures')
        url = f'{base_url}/json'
        params = {'date_from': date_from,
                  'time_from': time_from,
                  'date_to': date_to,
                  'time_to': time_to,
                  'component': component,
                  'scope': scope}

        if station is not None:
            params['station'] = station

        return self.get(url, params=params)

    def measures_components(self, respComponents, date_from, time_from='24', date_to='2999-12-31', time_to='24',
                            scope='2', selection=None, expand=None):
        """
        Request a list with all given information to the given scope.
        The Umweltbundesamt delivers inconsistent timestamps so their correctness is a little bit unclear. Seems that
        the one used as values is UTC+01:00 and the system works 1 hour delayed. The timestamp used as key could be
        UTC, but again not used by the search parameters.
        Args:
            selection: A list with a selection of the toplevel fields of interest.
            expand: Out of Order (TODO)

        Returns: A List with all available informations to given warnings.
        """
        genericCompDict = dict()
        for i in range(1, respComponents.get('count') + 1):
            # transfer given list to more comfortable dictionary
            compDescription = {
                'id': respComponents.get(str(i))[0],
                'code': respComponents.get(str(i))[1],
                'symbol': respComponents.get(str(i))[2],
                'unit': respComponents.get(str(i))[3],
                'name': respComponents.get(str(i))[4]
            }
            # get the measurements from all stations for the current component
            resp_measures = self.measures(date_from=date_from, time_from=time_from, date_to=date_to, time_to=time_to,
                                          scope=scope, component=compDescription['id'])

            for key, value in resp_measures['data'].items():
                if genericCompDict.get(key) is None:
                    # generate array with 2 rows -> first row with component description and the corresponding measurements in the second
                    genericCompDict[key] = {key2: {compDescription['id']: [compDescription, value2]} for (key2, value2)
                                            in value.items()}
                else:
                    for key2 in genericCompDict[key].keys():
                        # key2 = date
                        genericCompDict[key][key2][compDescription['id']] = {
                            compDescription['id']: [compDescription, value.get(key2)]}

        return genericCompDict

    def measures_stations(self,
                               respComponents,
                               date_from,
                               time_from='24',
                               date_to='2999-12-31',
                               time_to='24',
                               dict_scopes = {'1': '1TMW', '2': '1SMW', '3': '1SMW_MAX', '6': '1TMWGL'},
                               sleeptime=1, selection=None, expand=None):
        """
        Request a list with all given scope-based information.
        The Umweltbundesamt delivers inconsistent timestamps so their correctness is a little bit unclear. Seems that
        the one used as values is UTC+01:00 and the system works 1 hour delayed. The timestamp used as key could be
        UTC, but again not used by the search parameters.
        Scopes:
        2: 1SMW -> Ein-Stunden-Mittelwert
        3: 1SMW_MAX -> Ein-Stunden-Tagesmaxima
        6: 1TMWGL -> Tagesmittel stündlich gleitend
        1: 1TMW -> Tagesmittel (every day 12:00 utc+1)
        5: 8SMW_MAX -> 8h Tagesmaxima
        4: 8SMW -> 8h Mittelwert
        Args:
            selection: A list with a selection of the toplevel fields of interest.
            expand: Out of Order (TODO)

        Returns: A List with all available informations to given warnings.
        """

        # get stations respective to given time
        resp_stations = self.meta(date_from=date_from, time_from=time_from, date_to=date_to, time_to=time_to)
        dict_stations = resp_stations.get('stations')

        # new dictionary -> id
        l_stations_all = list()
        dict_stations_all = dict()
        for i in range(1, respComponents.get('count') + 1):
            # transfer given list to more comfortable dictionary
            # active: 1: PM10 (Particulate matter),3: 03 (Ozone), 5: NO2 (Nitrogen dioxide)
            comp_description = {
                'id': respComponents.get(str(i))[0],
                'code': respComponents.get(str(i))[1],
                'symbol': respComponents.get(str(i))[2],
                'unit': respComponents.get(str(i))[3],
                'name': respComponents.get(str(i))[4]
            }

            for (scope_key, scope_val) in dict_scopes.items():
                # get the measurements from all stations for the current component
                resp_measures_scope = self.measures(date_from=date_from, time_from=time_from, date_to=date_to, time_to=time_to,
                                                 scope=scope_key, component=comp_description['id'])
                if sleeptime is not None:
                    sleep(sleeptime)

                for station_id, l_station in dict_stations.items():
                    dict_data_scope = resp_measures_scope.get('data').get(station_id)

                    if dict_stations_all.get(station_id) is None and dict_data_scope is not None:
                        dict_stations_all[station_id] = {key_ts: {comp_description.get('code'): {scope_val: val_measure[2]}}
                                                         for (key_ts, val_measure) in dict_data_scope.items()}
                    elif dict_stations_all.get(station_id) is not None and dict_data_scope is not None:

                        for (key_ts, val_measure) in dict_data_scope.items():
                            # timestamp already in dictionary of this station
                            if (dict_stations_all[station_id].get(key_ts)):
                                if (dict_stations_all[station_id].get(key_ts).get(comp_description.get('code'))):
                                    dict_stations_all[station_id][key_ts][comp_description.get('code')].update({scope_val: val_measure[2]})
                                else:
                                    dict_stations_all[station_id][key_ts].update({comp_description.get('code'): {scope_val: val_measure[2]}})
                            else:
                                dict_stations_all[station_id][key_ts] = {comp_description.get('code'): {scope_val: val_measure[2]}}




        # transform dict to list after enrichment (lazy)
        for station_id, dict_station in dict_stations_all.items():
            for ts, measures in dict_station.items():
                 l_stations_all.append({'timestamp': ts, 'station_id': station_id, 'station_active_from': dict_stations.get(station_id)[5],
                                   'station_active_to':  dict_stations.get(station_id)[6], 'station_lat': dict_stations.get(station_id)[8],
                                   'station_lon': dict_stations.get(station_id)[7], 'measures': measures})

        return l_stations_all

    def components(self, lang='en'):
        """
        Retrieve all avaiable components given by the API of the Umweltbundesamt.
        Args:
            expand: Out of Order (TODO)

        Returns: List including the response.
        """
        base_url = self.resource_url(resource='components')
        url = f'{base_url}/json'
        params = {'lang': lang}

        return self.get(url, params=params)

    def meta(self, date_from, use='transgression', time_from='24', date_to='2999-12-31', time_to='24', lang='en'):
        """
        Retrieve active metadata including the stations given by the API of the Umweltbundesamt.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='meta')
        url = f'{base_url}/json'
        params = {'use': use,
                  'date_from': date_from,
                  'time_from': time_from,
                  'date_to': date_to,
                  'time_to': time_to,
                  'lang': lang}
        return self.get(url, params=params)

    def stations(self, expand=None):
        """
        Retrieve all oxygen measurement stations given by the API of the Umweltbundesamt.
        Args:
            expand: Out of Order (TODO)

        Returns: List with dictionaries including the response.
        """
        base_url = self.resource_url(resource='stations')
        url = f'{base_url}/json'
        params = {}
        if expand:
            params['expand'] = expand
        return self.get(url, params=params)

    JSON_SCHEMA_UMWELTBAMT_MEASURES = {
        'type': 'object',
        'properties': {
            'request': {'type': 'object'},
            'indices': {'type': 'object'},
            'data': {'type': 'object'},
        },
        'required': ['request', 'indices', 'data'],
        'additionalProperties': False
    }

    JSON_SCHEMA_UMWELTBAMT_COMPONENTS = {
        'type': 'object',
        'properties': {
            'count': {'type': 'number'},
            'indices': {'type': 'array'},
        },
        'required': ['count', 'indices'],
        'additionalProperties': True
    }

    JSON_SCHEMA_UMWELTBAMT_META = {
        'type': 'object',
        'properties': {
            'components': {'type': 'array'},
            'networks': {'type': 'object'},
            'stations': {'type': 'object'},
            'request': {'type': 'object'},
            'indices': {'type': 'object'},
        },
        'required': ['components', 'networks', 'stations', 'request', 'indices'],
        'additionalProperties': False
    }

    JSON_SCHEMA_UMWELTBAMT_STATIONS = {
        'type': 'object',
        'properties': {
            'request': {'type': 'object'},
            'indices': {'type': 'array'},
            'data': {'type': 'object'},
            'count': {'type': 'number'},
        },
        'required': ['request', 'indices', 'data', 'count'],
        'additionalProperties': False
    }
