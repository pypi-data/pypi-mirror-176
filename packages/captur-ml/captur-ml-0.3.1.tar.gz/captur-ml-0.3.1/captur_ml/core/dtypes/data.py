from pydantic.dataclasses import dataclass as pd_dataclass

from .image import Image
from .label import ClassLabel
from .prediction import PredictionSet


@pd_dataclass
class TrainingData:
    #: The list of images used for training
    images: list[Image]
    #: The list of class labels used for training
    labels: list[ClassLabel]


@pd_dataclass
class PredictionData:
    #: The list of images used for prediction
    images: list[Image]


@pd_dataclass
class EvaluationData:
    #: The list of images used for evaluation
    images: list[Image]
    #: The list of class labels used for evaluation
    labels: list[ClassLabel]
    #: The list of classification predictions used for evaluation
    predictions: PredictionSet
