from pydantic import root_validator
from pydantic.dataclasses import dataclass as pd_dataclass
from typing import Any, Literal

from .base import BaseStorageFolder
from captur_ml.core.exceptions import GoogleCloudStorageBucketNotFoundError
from captur_ml.core.utils.path import is_storage_gs_uri, get_bucket_from_gs_uri
from captur_ml.core.services.gcs import (
    _get_storage_client,
    write_file_to_gcs,
    write_json_to_gcs,
    write_jsonl_to_gcs,
    read_file_from_gcs,
    delete_file_from_gcs,
    check_file_exists,
    check_bucket_exists,
)


__pdoc__ = {
    "GCSFolder.bucket_exists": False,
}


@pd_dataclass
class GCSFolder(BaseStorageFolder):
    """A Google Cloud Storage folder."""

    #: The path to the folder in Google Cloud Storage.
    folder_path: str

    #: If true, run preflight checks on the folder path.
    check_exists: bool = True

    #: The client object used to interact with Google Cloud Storage.
    client = None

    def __post_init__(self):
        if self.client is None:
            self.client = _get_storage_client()

    @root_validator()
    def bucket_exists(cls, values):
        if values.get("check_exists") is False:
            return values

        full_path = values.get("folder_path")
        if not is_storage_gs_uri(full_path):
            raise ValueError(
                f"Expected a Google Cloud Storage URI, but received {full_path}"
            )

        bucket_name = get_bucket_from_gs_uri(full_path)
        if bucket_name is None or not check_bucket_exists(
            bucket_name, storage_client=values.get("client")
        ):
            raise GoogleCloudStorageBucketNotFoundError(
                f"The bucket {bucket_name} does not exist."
            )

        return values

    @property
    def bucket_name(self) -> str:
        """The name of the Google Cloud Storage bucket."""
        return get_bucket_from_gs_uri(self.folder_path)

    def write(self, file_contents: str | bytes, destination_filename: str):
        """Writes a file of either string or bytes content type to Google Cloud Storage.

        Args:
            file_contents (str | bytes): The contents of the file to write to Google Cloud Storage.
            destination_filename (str): The name of the file to write to Google Cloud Storage.

        Raises:
            GoogleCloudStorageResourceNotFoundError: If the Google Cloud Storage bucket does not exist.
        """
        if destination_filename.endswith(".json"):
            self._write_json(
                json_dict=file_contents,
                destination_filename=destination_filename,
            )
        elif destination_filename.endswith(".jsonl"):
            self._write_jsonl(
                json_lines=file_contents,
                bucket_name=self.bucket_name,
                destination_filename=destination_filename,
            )
        else:
            write_file_to_gcs(
                file_contents=file_contents,
                bucket_name=self.bucket_name,
                destination_filename=destination_filename,
                storage_client=self.client,
            )

    def _write_json(self, json_dict: dict[Any, Any], destination_filename: str):
        """Writes a JSON file to Google Cloud Storage.

        Args:
            json_dict (dict[Any, Any]): The dictionary to export as JSON to Google Cloud Storage.
            destination_filename (str): The name of the file to write to Google Cloud Storage. If it does not end with the .json extension, it will be added.

        Raises:
            ValueError: If the dictionary cannot be serialized to JSON.
        """
        write_json_to_gcs(
            json_dict=json_dict,
            bucket_name=self.bucket_name,
            destination_filename=destination_filename,
            storage_client=self.client,
        )

    def _write_jsonl(self, json_lines: list[dict[Any, Any]], destination_filename: str):
        """Writes a JSONL file to Google Cloud Storage.

        Args:
            json_lines (list[dict]): The list of dictionaries to export as JSONL to Google Cloud Storage.
            destination_filename (str): The name of the file to write to Google Cloud Storage. If it does not end with the .jsonl extension, it will be added.

        Raises:
            ValueError: If the dictionary cannot be serialized to JSON.
        """
        write_jsonl_to_gcs(
            json_lines=json_lines,
            bucket_name=self.bucket_name,
            destination_filename=destination_filename,
            storage_client=self.client,
        )

    def read(
        self, origin_filename: str, read_mode: Literal["r", "b"] = "r"
    ) -> bytes | str:
        """Reads a file from Google Cloud Storage.

        Args:
            origin_filename (str): The name of the file to read from Google Cloud Storage.
            read_mode (Literal["r", "b"], optional): The mode to read the file in. "r" for text, "b" for bytes. Defaults to "r".

        Raises:
            GoogleCloudStorageResourceNotFoundError: If the Google Cloud Storage bucket or file does not exist.
            ValueError: If the read_mode is not "b" but the file cannot be decoded as UTF-8.

        Returns:
            bytes | str: The raw contents of the file.
        """
        return read_file_from_gcs(
            bucket_name=self.bucket_name,
            origin_filename=origin_filename,
            read_mode=read_mode,
            storage_client=self.client,
        )

    def delete(self, destination_filename: str):
        """Deletes a file from Google Cloud Storage.

        Args:
            destination_filename (str): The name of the file to delete from Google Cloud Storage.

        Raises:
            GoogleCloudStorageResourceNotFoundError: If the Google Cloud Storage bucket or file does not exist.
        """
        delete_file_from_gcs(
            bucket_name=self.bucket_name,
            destination_filename=destination_filename,
            storage_client=self.client,
        )

    def contains(self, filename: str) -> bool:
        return check_file_exists(
            bucket_name=self.bucket_name,
            filename=filename,
            storage_client=self.client,
        )
