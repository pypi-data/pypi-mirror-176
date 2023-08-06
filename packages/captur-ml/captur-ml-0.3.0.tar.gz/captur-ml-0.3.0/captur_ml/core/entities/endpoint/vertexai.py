from pydantic.dataclasses import dataclass

from google.cloud.aiplatform import Endpoint
from google.cloud.aiplatform_v1beta1.types import DeployedModel

from google.api_core import exceptions as google_exceptions

from .base import BaseEndpoint
from captur_ml.core.exceptions import (
    GoogleCloudVertexAIEndpointDoesNotExistError,
    GoogleCloudVertexAIEndpointNoModelDeployedError,
)


@dataclass
class VertexAIEndpoint(BaseEndpoint):
    """An object that represents a Vertex AI endpoint. An endpoint is a deployed model that can be used for prediction."""

    #: The GCP project name.
    project: str
    #: The global location of the VertexAI Endpoint.
    location: str
    #: Run checks to see if the endpoint exists and is active on initialization.
    check_on_init: bool = False

    def __post_init__(self):
        self.endpoint = Endpoint(
            endpoint_name=self.id, project=self.project, location=self.location
        )

        if self.check_on_init:
            if not self.exists:
                raise GoogleCloudVertexAIEndpointDoesNotExistError()
            if not self.is_active:
                raise GoogleCloudVertexAIEndpointNoModelDeployedError()

    @property
    def exists(self) -> bool:
        """Checks if the VertexAI Endpoint exists."""
        try:
            self.endpoint.list_models()
        except (google_exceptions.NotFound, google_exceptions.InvalidArgument):
            return False
        return True

    @property
    def is_active(self) -> bool:
        """Checks if the VertexAI Endpoint exists and has at least one model serving requests."""
        if not self.exists:
            return False

        return len(self.models) > 0

    @property
    def models(self) -> list[DeployedModel]:
        """Returns a list of models deployed to the VertexAI Endpoint."""
        return self.endpoint.list_models()
