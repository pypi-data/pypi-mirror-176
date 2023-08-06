from enum import Enum
from pydantic.dataclasses import dataclass as pd_dataclass

from captur_ml.core.dtypes import ImageOrImageList
from captur_ml.core.entities.endpoint import Endpoint
from captur_ml.core.services.aiplatform.live_predict import (
    get_image_classification_prediction_from_deployed_automl,
    convert_automl_to_captur,
)
from captur_ml.core.dtypes.result import ImageClassificationResult


class PredictionService(Enum):
    AUTOML = "automl"


@pd_dataclass
class LivePredictionJobConfig:
    """
    Configuration for a live prediction job.
    """
    #: The endpoint to use for the prediction.
    endpoint: Endpoint


class LivePredictionJob:
    """
    A live prediction job is a job that runs on an image or set of images and returns the results of the prediction job. It is first initialized with a configuration object and then started with the chosen image(s).
    """
    def __init__(self, config: LivePredictionJobConfig):
        self.config = config
        self.service: PredictionService = PredictionService.AUTOML

    def start(self, images: ImageOrImageList) -> list[ImageClassificationResult]:
        """Starts the (sync) live prediction job.

        Args:
            images (ImageOrImageList): The images to predict on.

        Returns:
            list[ImageClassificationResult]: The result of the prediction job.
        """
        match self.service:
            case PredictionService.AUTOML:
                result = get_image_classification_prediction_from_deployed_automl(
                    images=images,
                    endpoint=self.config.endpoint,
                )
                result = convert_automl_to_captur(images, result)

                return result
