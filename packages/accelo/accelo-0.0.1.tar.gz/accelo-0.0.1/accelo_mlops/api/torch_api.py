from dataclasses import asdict
import requests
from requests.exceptions import ConnectionError, HTTPError
from accelo_mlops.utils.errors import MLOpsAPIError, TorchAPIError
from accelo_mlops.utils.constants import (ACCELO_API_ENDPOINT, ACCELO_API_ACCESS_KEY, ACCELO_API_SECRET_KEY)
import os
import logging
env = os.environ
_logger = logging.getLogger(__name__)


class TorchApi:

    BASE_URL = f'https://{ACCELO_API_ENDPOINT}:5443/catalog-server/api'
    HEADERS = {
        'accessKey': ACCELO_API_ACCESS_KEY,
        'secretKey': ACCELO_API_SECRET_KEY,
        'Content-Type': 'application/json'
    }

    @classmethod
    def create_assembly(cls, assembly):
        _logger.debug(f'DEBUG: Registering project = {assembly.name}')
        assembly_url = f'{cls.BASE_URL}/assemblies'
        data = {
            'assembly': asdict(assembly)
        }
        try:
            response = requests.post(url=assembly_url, json=data, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: Register project response for project name = {assembly.name} : {response.json()}')
            if not response.ok:
                raise MLOpsAPIError(f'Unknown error occurred: Response from API: {response.text}')
        except ConnectionError as ce:
            raise TorchAPIError('Some error occurred when trying to create a project. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError('Some error occurred when trying to create a project. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def initialize_snapshot(cls, snapshot):
        _logger.debug(f'DEBUG: Initializing snapshot for project id = {snapshot.associatedItemId}')
        snapshot_url = f'{cls.BASE_URL}/snapshots/initialise'
        data = {
            'data': asdict(snapshot)
        }
        try:
            response = requests.post(url=snapshot_url, json=data, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: Register model response for project id = {snapshot.associatedItemId} : {response.json()}')
            if not response.ok:
                raise TorchAPIError(f'Unknown error occurred: Response from API: {response.text}')
        except ConnectionError as ce:
            raise TorchAPIError('Some error occurred when trying to initialize the project. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError('Some error occurred when trying to initialize the project. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def register_asset(cls, asset):
        asset_url = f'{cls.BASE_URL}/assets'
        data = {
            'data': asdict(asset)
        }
        try:
            response = requests.put(url=asset_url, json=data, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: Register model response for asset = {asset} : {response.json()}')
            if not response.ok:
                raise TorchAPIError(f'Unknown error occurred: Response from API: {response.text}')
        except ConnectionError as ce:
            raise TorchAPIError('Some error occurred when trying to register the model artifacts. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError('Some error occurred when trying to register the model artifacts. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def get_asset_metadata(cls, asset_id):
        _logger.debug(f'DEBUG: Getting asset metadata for asset id = {asset_id}')
        metadata_url = f'{cls.BASE_URL}/assets/{asset_id}/metadata'
        try:
            response = requests.get(url=metadata_url, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: metadata response for asset id = {asset_id} : {response.json()}')
        except ConnectionError as ce:
            raise TorchAPIError(f'Some error occurred when trying to get the asset with id={asset_id}. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError(f'Some error occurred when trying to get the asset with id={asset_id}. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def add_metadata(cls, asset_id, metadata):
        _logger.debug(f'DEBUG: Adding metadata for asset id = {asset_id}')
        metadata_url = f'{cls.BASE_URL}/assets/{asset_id}/metadata'
        try:
            response = requests.put(url=metadata_url, json=metadata, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: Metadata add response = {response.json()}')
            if not response.ok:
                raise TorchAPIError(f'Unknown error occurred: Response from API: {response.text}')
        except ConnectionError as ce:
            raise TorchAPIError('Some error occurred when trying to register the model artifacts. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError('Some error occurred when trying to register the model artifacts. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def update_asset_metadata(cls, asset_id, new_metadata):
        _logger.debug(f'DEBUG: Updating metadata for asset id = {asset_id}')
        required_fields = ['assetId', 'currentSnapshot', 'items', 'snapshots']

        if cls.is_asset_exists(asset_id):
            current_metadata = cls.get_asset_metadata(asset_id)
            data = {key: value for key, value in current_metadata.get('data').items() if key in required_fields}
            curr_snapshot = current_metadata.get('data').get('currentSnapshot')
            if 'snapshots' in data and curr_snapshot not in data['snapshots']:
                data['snapshots'].append(curr_snapshot)
            else:
                data['snapshots'] = [curr_snapshot]
            request_payload = {'data': data}
            request_payload['data']['items'].extend([asdict(m) for m in new_metadata])
            _logger.debug(f'DEBUG: Metadata info = {request_payload}')
            cls.add_metadata(asset_id, request_payload)

    @classmethod
    def get_asset(cls, asset_id):
        _logger.debug(f'DEBUG: Getting asset id = {asset_id} details. ')
        asset_url = f'{cls.BASE_URL}/assets/{asset_id}/overview'
        try:
            response = requests.get(url=asset_url, headers=cls.HEADERS, allow_redirects=False, verify=False)
        except ConnectionError as ce:
            raise TorchAPIError(f'Some error occurred when trying to get the asset with id={asset_id}. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError(f'Some error occurred when trying to get the asset with id={asset_id}. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def get_snapshot(cls, assembly_id):
        _logger.debug(f'DEBUG: Getting snapshot details for project id = {assembly_id}')
        snapshot_url = f'{cls.BASE_URL}/snapshots/{assembly_id}'
        try:
            response = requests.get(url=snapshot_url, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: Current snapshot response for project id = {assembly_id}: {response.json()}')
        except ConnectionError as ce:
            raise TorchAPIError('Some error occurred when trying to get the current snapshot. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError('Some error occurred when trying to get the current snapshot. '
                                f'Response from the API: {str(http_err)}')
        return response.json()[0]

    @classmethod
    def current_snapshot(cls, assembly_id):
        _logger.info(f'INFO: Current snapshot for project id = {assembly_id}')
        return cls.get_snapshot(assembly_id).get('uuid', {'errors': True})

    @classmethod
    def get_assembly_by_id(cls, assembly_id):
        assembly_url = f'{cls.BASE_URL}/assemblies/{assembly_id}'
        try:
            response = requests.get(url=assembly_url, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: Current project response for project = {assembly_id} : {response.json()}')
        except ConnectionError as ce:
            raise TorchAPIError(f'Some error occurred when trying to get the assembly with id={assembly_id}. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError(f'Some error occurred when trying to get the assembly with id={assembly_id}. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def get_assembly_by_name(cls, assembly_name):
        _logger.debug(f'DEBUG: Get project details by project name = {assembly_name}')
        assembly_url = f'{cls.BASE_URL}/assemblies?name={assembly_name}'
        try:
            response = requests.get(url=assembly_url, headers=cls.HEADERS, allow_redirects=False, verify=False)
            _logger.debug(f'DEBUG: Project response for project name = {assembly_name} : {response.json()}')
        except ConnectionError as ce:
            raise TorchAPIError(f'Some error occurred when trying to get the assembly with name={assembly_name}. '
                                f'Response from the API: {str(ce)}')
        except HTTPError as http_err:
            raise TorchAPIError(f'Some error occurred when trying to get the assembly with name={assembly_name}. '
                                f'Response from the API: {str(http_err)}')
        return response.json()

    @classmethod
    def get_assembly_name(cls, assembly_id):
        _logger.info(f'INFO: Current assembly id = {assembly_id}')
        return cls.get_assembly_by_id(assembly_id).get('data').get('name')

    @classmethod
    def is_asset_exists(cls, asset_id):
        _logger.debug(f'DEBUG: Checking if asset id = {asset_id} exists. ')
        if not cls.get_asset(asset_id).get('errors'):
            return True
        return False

    @classmethod
    def is_assembly_exists(cls, assembly_id=None, assembly_name=None):
        if assembly_id:
            _logger.debug(f'DEBUG: Searching project by id = {assembly_id}')
            if 'errors' not in cls.get_assembly_by_id(assembly_id):
                return True
        elif assembly_name:
            _logger.debug(f'DEBUG: Searching project by name = {assembly_name}')
            if cls.get_assembly_by_name(assembly_name).get('data'):
                return True
        return False
