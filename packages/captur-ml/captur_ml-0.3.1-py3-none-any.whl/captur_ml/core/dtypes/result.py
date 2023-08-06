from dataclasses_json import dataclass_json, LetterCase
from pydantic.dataclasses import dataclass as pd_dataclass

from captur_ml.core.dtypes.generic import ObjectWithId
from captur_ml.core.dtypes.prediction import ClassPrediction


@dataclass_json(letter_case=LetterCase.CAMEL)
@pd_dataclass
class ImageClassificationResult(ObjectWithId):
    """The set of predictions for an image."""

    #: The set of predictions for the image.
    predictions: list[ClassPrediction]
