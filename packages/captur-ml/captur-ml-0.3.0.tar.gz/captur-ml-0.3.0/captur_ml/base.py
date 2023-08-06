from pydantic.dataclasses import dataclass as pd_dataclass

from captur_ml.predict import PredictionJobConfig, LivePredictionJob, BatchPredictionJob, LivePredictionJobConfig, BatchPredictionJobConfig
from captur_ml.core.dtypes import ImageOrImageList


@pd_dataclass
class CapturMLConfig:
    """
    Configuration for the CapturML client.
    """
    pass


class CapturML:
    """
    The CapturML class is the main entry point for the CapturML machine learning library. It unifies the APIs for the different machine learning tasks (training, evaluation, prediction) and provides a single interface to interact with.
    """
    def __init__(self, config: CapturMLConfig | None = None):
        self.config = config

    def predict(self, images: ImageOrImageList, config: PredictionJobConfig):
        """Generates predictions for an image or a set of images.

        Args:
            images (ImageOrImageList): The images to predict on.
            config (PredictionJobConfig): A configuration object for the prediction job. The choice of configuration object depends on the type of prediction job and will determine the type of prediction job.

        Raises:
            ValueError: If the prediction job config is not of a known type.

        Returns:
            Any: The result of the prediction job. If the prediction job is a live prediction job, the result will be a list of predictions. If the prediction job is a batch prediction job, the result will be a promise type object that can be used to retrieve the result of the prediction job.
        """
        match config:
            case LivePredictionJobConfig():
                job = LivePredictionJob(config)
            case BatchPredictionJobConfig():
                job = BatchPredictionJob(config)
            case other:
                raise ValueError(f"Unknown prediction job config type: {other}. Supported types are: 'LivePredictionJobConfig', 'BatchPredictionJobConfig'")
        
        return job.start(images)

    def train(self, images: ImageOrImageList, config):
        """This is a stub method for training a model.

        Args:
            images (ImageOrImageList): The images to train on.
            config (TrainingJobConfig): A configuration object for the training job.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError()
    
    def evaluate(self, images: ImageOrImageList, config):
        """This is a stub method for evaluating a model.
            
            Args:
                images (ImageOrImageList): The images to evaluate on.
                config (EvaluationJobConfig): A configuration object for the evaluation job.
    
            Raises:
                NotImplementedError
            """
        raise NotImplementedError()
