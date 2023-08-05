import numpy as np
import pandas as pd
from typing import Optional, List, Union
from dataclasses import dataclass


@dataclass
class Baseline:
    model_id: str
    model_version: int
    baseline_data: Optional[pd.DataFrame]
    labels: Union[List, np.ndarray, pd.Series]
    label_name: str
    entity_type: str = 'data'
    sub_entity_type: str = 'baselines'
