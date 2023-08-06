from abc import ABC
from pydantic.dataclasses import dataclass


@dataclass
class BaseStorageFolder(ABC):
    """A base class for storage folders. Storage folders are used to store images and other files."""

    folder_path: str

    def write(self, file_contents: str, destination_filename: str):
        pass

    def read(self, filename: str):
        pass

    def delete(self, filename: str):
        pass

    def contains(self, filename: str) -> bool:
        pass
