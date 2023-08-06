"""Predict."""

import typing as t
from typing import Any
from typing import Dict

import numpy as np
import pandas as pd

from house_sales import __version__ as _version
from house_sales.config.core import config
from house_sales.processing.data_manager import load_pipeline
from house_sales.processing.validation import validate_inputs


pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_price_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, Dict[Any, Any]],
) -> Dict[Any, Any]:
    """Make a prediction using a saved model pipeline."""
    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _price_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": [np.exp(pred) for pred in predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results
