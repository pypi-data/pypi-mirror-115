from dataclasses import dataclass
from dataclasses import field
from dataclasses import asdict
import json
from accelo_mlops.utils.constants import ACCELO_API_ENDPOINT


@dataclass
class SourceType:
    id: int = 20
    name: str = 'MODEL_BAG'


@dataclass
class Assembly:
    name: str
    sourceType: SourceType = field(default_factory=lambda: SourceType())
    description: str = 'This is a default description. '
    isVirtual: bool = True


class AssemblyToProjectResponse:

    @staticmethod
    def convert(assembly_response):
        response = {}
        response_keys = ['id', 'name', 'description', 'createdAt']
        if isinstance(assembly_response.get('data'), list):
            assembly_items = assembly_response.get('data')[0].items()
        else:
            assembly_items = assembly_response.get('data').items()
        for key, value in assembly_items:
            if key in response_keys:
                if key == 'id':
                    response['project_id'] = value
                else:
                    response[key] = value
        response['url'] = f'https://{ACCELO_API_ENDPOINT}:5443/data-catalog/data-sources'
        return response
