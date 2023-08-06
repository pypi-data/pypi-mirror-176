from dataclasses import field
from pydantic.dataclasses import dataclass as pd_dataclass

from captur_ml.core.dtypes.generic import NamedObjectWithId, ObjectWithId


@pd_dataclass
class ClassLabel(NamedObjectWithId):
    """The classification label that describes the semantic meaning of an observation."""

    pass


@pd_dataclass
class AuditLabel(ObjectWithId):
    """A set of label that describes the acceptable classes of an observation during the audit process."""

    #: A list of human readable audit labels
    labels: list[ClassLabel] = field(default_factory=list)


@pd_dataclass
class BoundingBoxLabel(NamedObjectWithId):
    """The bounding box label that describes the semantic meaning of region in an observation."""

    #: The x-coordinate of the top-left corner of the bounding box
    x: float
    #: The y-coordinate of the top-left corner of the bounding box
    y: float
    #: The width of the bounding box
    width: float
    #: The height of the bounding box
    height: float
