from typing import TypeAlias

from .image import Image
from .label import ClassLabel, AuditLabel, BoundingBoxLabel
from .prediction import ClassPrediction, PredictionSet

ImageOrImageList: TypeAlias = Image | list[Image]
Label: TypeAlias = ClassLabel | AuditLabel | BoundingBoxLabel

__all__ = [
    "AuditLabel",
    "ClassLabel",
    "ClassPrediction",
    "PredictionSet",
    "Image",
    "ImageOrImageList",
    "Label",
]
