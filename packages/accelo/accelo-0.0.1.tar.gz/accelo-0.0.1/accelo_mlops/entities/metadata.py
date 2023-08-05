from dataclasses import dataclass
from dataclasses import field
from typing import List


@dataclass
class Metadata:
    key: str
    value: str
    dataType: str = 'STRING'


@dataclass
class MetadataList:
    metadata: List[Metadata] = field(default_factory=lambda: [])
