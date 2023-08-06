from pydantic.dataclasses import dataclass as pd_dataclass

from captur_ml.core.dtypes import ImageOrImageList


@pd_dataclass
class BatchPredictionJobConfig:
    """
    Configuration for a batch prediction job.
    """

    #: The root directory in the cloud where the various files for the batch prediction job will be stored.
    root_directory: str


class BatchPredictionJob:
    """
    A batch prediction job is a job that runs on a batch of images and returns a promise type object that can be used to retrieve the result of the prediction job. It is first initialized with a configuration object and then started with a list of images.
    """

    def __init__(self, config: BatchPredictionJobConfig):
        self.config = config

    def start(self, images: ImageOrImageList):
        """Starts the (async) batch prediction job.

        Args:
            images (ImageOrImageList): The images to predict on.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()
