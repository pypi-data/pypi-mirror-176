from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass

from captur_ml.core.dtypes.generic import ObjectWithId


@dataclass
class BaseEndpoint(ABC, ObjectWithId):
    """A base class for endpoints. Endpoints are used to make predictions on images."""

    @property
    @abstractmethod
    def exists(self):
        pass

    @property
    @abstractmethod
    def is_active(self):
        pass

    @property
    @abstractmethod
    def models(self):
        pass
