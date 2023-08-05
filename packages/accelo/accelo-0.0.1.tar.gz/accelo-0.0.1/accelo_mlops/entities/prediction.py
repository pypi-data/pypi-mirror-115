import numpy as np
import pandas as pd
from typing import Union, Optional, List
from dataclasses import dataclass


@dataclass
class Predictions:
    model_id: str
    model_version: int
    prediction_ids: List
    predictions: Union[List, np.ndarray, pd.Series]
    feature_data: Optional[pd.DataFrame] = None
    label_col: Optional[str] = None
    entity_type: str = 'data'
    sub_entity_type: str = 'predictions'
