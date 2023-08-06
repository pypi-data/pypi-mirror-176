from typing import TypeAlias

from .batch import BatchPredictionJob, BatchPredictionJobConfig
from .live import LivePredictionJob, LivePredictionJobConfig

PredictionJobConfig: TypeAlias = BatchPredictionJobConfig | LivePredictionJobConfig

__all__ = [
    "BatchPredictionJob",
    "LivePredictionJob",
    "PredictionJobConfig",
]
