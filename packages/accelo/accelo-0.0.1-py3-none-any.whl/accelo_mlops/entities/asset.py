from dataclasses import dataclass
from dataclasses import field
from typing import List
from accelo_mlops.entities.metadata import Metadata
from accelo_mlops.utils.constants import ACCELO_API_ENDPOINT


@dataclass
class MLSourceType:
    id: int = 20
    name: str = 'MODEL_BAG'
    type: str = 'ASSEMBLY'


@dataclass
class MLAssetType:
    id: int = 20
    name: str = 'ML_MODEL'


@dataclass
class Asset:
    name: str
    assemblyId: int
    currentSnapshot: str
    uid: str = 'Demo.UID.Change.It'
    assetTypeId: int = field(default=MLAssetType.id)
    sourceTypeId: int = field(default=MLSourceType.id)
    description: str = 'This is a default description. '
    isCustom: bool = False
    snapshots: List = field(default_factory=lambda: [])
    metadata: List[Metadata] = field(default_factory=lambda: [])


class AssetToModelResponse:

    @staticmethod
    def convert(asset_response):
        response = {}
        response_keys = ['id', 'name', 'description', 'uid']
        data = asset_response.get('data')
        for key, value in data.items():
            if key in response_keys:
                if key == 'id':
                    response['model_id'] = value
                else:
                    response[key] = value
        response['url'] = f'https://{ACCELO_API_ENDPOINT}:5443/catalog/discover/overview/{data.get("id")}'
        return response
