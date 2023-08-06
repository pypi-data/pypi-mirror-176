import re
from captur_ml.core.exceptions import (
    GoogleCloudVertexAIEndpointCorruptedImageError,
    GoogleCloudVertexAIEndpointDoesNotExistError,
    GoogleCloudVertexAIEndpointImageTooLargeError,
    GoogleCloudVertexAIEndpointNoModelDeployedError,
)
from captur_ml.core.entities import VertexAIEndpoint
from captur_ml.core.dtypes import Image, ImageOrImageList
from captur_ml.core.dtypes.result import ImageClassificationResult
from captur_ml.core.dtypes.prediction import ClassPrediction

from google.cloud import aiplatform_v1
from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as google_exceptions
from google.cloud.aiplatform.gapic import PredictionServiceClient, schema


def get_image_classification_prediction_from_deployed_automl(
    images: ImageOrImageList,
    endpoint: VertexAIEndpoint,
    prediction_service_client_options: ClientOptions | None = None,
    run_preflight_checks: bool = False,
) -> aiplatform_v1.types.PredictResponse:
    """Gets image classification prediction from deployed automl model.

    Args:
        images (ImageOrImageList): The Image(s) to predict for.
        endpoint (VertexAIEndpoint): VertexAIEndpoint object instance that will be used to make the prediction.
        prediction_service_client_options (ClientOptions | None): Client options to pass to the prediction service client. Default = None.
        run_preflight_checks (bool): Whether to run preflight checks on the endpoint. Default = False.

    Raises:
        `captur_ml.core.exceptions.GoogleCloudVertexAIEndpointDoesNotExistError`: If the specified endpoint does not exist.
        `captur_ml.core.exceptions.GoogleCloudVertexAIEndpointNoModelDeployedError`: If there is no model deployed at the specified endpoint.
        `captur_ml.core.exceptions.GoogleCloudVertexAIEndpointImageTooLargeError`: If the image exceeds the 1.5MB limit.

    Returns:
        automl_v1beta1.types.PredictResponse: An object containing the prediction results for the image.
    """
    if run_preflight_checks:
        if not endpoint.exists:
            raise GoogleCloudVertexAIEndpointDoesNotExistError()
        if not endpoint.is_active:
            raise GoogleCloudVertexAIEndpointNoModelDeployedError()

    if prediction_service_client_options is None:
        prediction_service_client_options = {
            "api_endpoint": f"{endpoint.location}-aiplatform.googleapis.com"
        }

    client = PredictionServiceClient(client_options=prediction_service_client_options)

    if isinstance(images, Image):
        images = [images]

    instances = [
        schema.predict.instance.ImageClassificationPredictionInstance(
            content=image.bytes,
        ).to_value()
        for image in images
    ]

    parameters = schema.predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.0,
        max_predictions=10,
    ).to_value()

    endpoint = client.endpoint_path(
        project=endpoint.project,
        location=endpoint.location,
        endpoint=endpoint.id,
    )

    try:
        response = client.predict(
            endpoint=endpoint, instances=instances, parameters=parameters
        )
    except google_exceptions.FailedPrecondition as e:
        match = re.search(r"exceeds (\d*.*) limit", e.message)
        if match:
            raise GoogleCloudVertexAIEndpointImageTooLargeError()
        else:
            raise e
    except google_exceptions.InvalidArgument as e:
        raise GoogleCloudVertexAIEndpointCorruptedImageError()

    return response


def convert_automl_to_captur(
    images: ImageOrImageList, prediction_response: aiplatform_v1.types.PredictResponse
) -> list[ImageClassificationResult]:
    """Converts the automl_v1beta1.types.PredictResponse object to a captur_ml.core.dtypes.result.ImageClassificationResult object.

    Returns:
        `captur_ml.core.dtypes.result.ImageClassificationResult`: The converted object.
    """
    if isinstance(images, Image):
        images = [images]

    predictions = list(zip(images, prediction_response.predictions))

    results = []
    for image, prediction in predictions:
        ids = prediction["ids"]
        class_names = prediction["displayNames"]
        confidences = prediction["confidences"]

        predictions = []
        for id, name, confidence in zip(ids, class_names, confidences):
            pred = ClassPrediction(
                id=id,
                name=name,
                confidence=confidence,
            )
            predictions.append(pred)

        predictions.sort(key=lambda x: x.confidence, reverse=True)

        result = ImageClassificationResult(id=image.id, predictions=predictions)
        results.append(result)

    return results
