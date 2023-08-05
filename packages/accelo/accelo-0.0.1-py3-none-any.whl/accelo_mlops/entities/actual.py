import numpy as np
import pandas as pd
from typing import Union, List, Optional
from dataclasses import dataclass


@dataclass
class Actuals:
    model_id: str
    model_version: int
    actual_ids: List
    actuals: Optional[Union[List, np.ndarray, pd.Series]]
    label_col: Optional[str] = None
    entity_type: str = 'data'
    sub_entity_type: str = 'actuals'
