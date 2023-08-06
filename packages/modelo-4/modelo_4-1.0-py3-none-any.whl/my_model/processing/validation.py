from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from my_model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if validated_data[var].isnull().sum() > 0
        #if var not in config.model_config.numerical_vars_with_na
        #and validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data

## meter funcion para filtrar segun rangos intervalos razonables


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleGenderDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class DataInputSchema(BaseModel):
    alcohol: Optional[float]
    fixed_acidity: Optional[float]
    volatile_acidity: Optional[float]
    residual_sugar: Optional[float]
    fixed_acidity: Optional[float]
    chlorides: Optional[float]
    free_sulfur_dioxide: Optional[float]
    total_sulfur_dioxide: Optional[float]
    density: Optional[float]
    pH: Optional[float]
    sulphates: Optional[float]


class MultipleGenderDataInputs(BaseModel):
    inputs: List[DataInputSchema]