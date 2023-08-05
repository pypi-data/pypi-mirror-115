from dataclasses import dataclass


@dataclass
class Model:
    id: int
    name: str
    version: str
    project_id: int
    model_object: object
    model_location: str = None
    hyperparams: dict = None
    model_type: str = None
    error_metric: str = None
    model_results: dict = None
    entity_type: str = 'models'
    sub_entity_type: str = None
