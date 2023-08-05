from dataclasses import dataclass


@dataclass
class Feature:
    entity_type: str = 'data'
    sub_entity_type: str = 'feature'
