from typing import TypeAlias
from pydantic.dataclasses import dataclass as pd_dataclass

from captur_ml.core.dtypes.generic import ObjectWithId, WithConfidence
from captur_ml.core.dtypes.label import ClassLabel, BoundingBoxLabel


@pd_dataclass
class ClassPrediction(ClassLabel, WithConfidence):
    """A class prediction with a confidence score."""


@pd_dataclass
class BoundingBoxPrediction(BoundingBoxLabel, WithConfidence):
    """A bounding box prediction with a confidence score."""


Prediction: TypeAlias = ClassPrediction | BoundingBoxPrediction


@pd_dataclass
class PredictionSet(ObjectWithId):
    """A set of predictions."""

    #: A list of predictions
    predictions: list[Prediction]
