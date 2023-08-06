from uuid import uuid4
from pydantic import confloat
from pydantic.dataclasses import dataclass as pd_dataclass


# The kw_only flag is set here to force the use of keyword arguments
# for the dataclass constructor. This is to avoid
#       TypeError: non-default argument '___' follows default argument


@pd_dataclass(kw_only=True)
class ObjectWithId:
    """This generic class automatically adds an id field to the dataclass.
    If the id field is not provided, it will be automatically generated as a UUID, using uuid4() from the Python uuid module.
    """

    #: A unique identifier of the object.
    id: str | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid4())


@pd_dataclass(kw_only=True)
class NamedObjectWithId(ObjectWithId):
    """This is a variant of the `captur_ml.core.dtypes.generic.ObjectWithId` class, which requires a name field."""

    #: A human-readable name of the object
    name: str


@pd_dataclass(kw_only=True)
class WithConfidence:
    """A generic object with a confidence score."""

    #: The statistical confidence of the Prediction. Must be between 0 and 1.
    confidence: confloat(ge=0, le=1)
