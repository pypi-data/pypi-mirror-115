from dataclasses import dataclass


@dataclass
class Snapshot:
    associatedItemId: int
    uuid: str
    associatedItemType: str = 'ASSEMBLY'
