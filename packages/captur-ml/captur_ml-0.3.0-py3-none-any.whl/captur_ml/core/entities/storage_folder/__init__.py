from typing import TypeAlias

from .gcs import GCSFolder

StorageFolder: TypeAlias = GCSFolder  # For future: GCSFolder | ...

__all__ = ["StorageFolder", "GCSFolder"]
