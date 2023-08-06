from pydantic import AnyUrl, root_validator
from pydantic.dataclasses import dataclass as pd_dataclass

from captur_ml.core.dtypes.generic import ObjectWithId
from captur_ml.core.utils.image import load_image_bytes_from_url
from captur_ml.core.utils.path import get_gs_uri_from_uri


__pdoc__ = {
    "Image.must_contain_url_or_data": False,
    "Image.infer_mime": False,
}

MIME_TYPES = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "tiff": "image/tiff",
    "tif": "image/tiff",
    "bmp": "image/bmp",
    "gif": "image/gif",
}


@pd_dataclass
class Image(ObjectWithId):
    """An image with optional metadata."""

    #: The image bytes encoded as a UTF-8 string. Required if `url` is not specified.
    data: str = ""
    #: An http[s]:// or gs:// URL pointing to the image resource. Required if `data` is not specified.
    url: AnyUrl | None = None
    #: The MIME type of the image. Required if `data` is specified.
    mime_type: str | None = None

    @root_validator
    def must_contain_url_or_data(cls, values):
        if not values.get("url") and not values.get("data"):
            raise ValueError("Either `url` or `data` must be specified.")
        return values

    @root_validator
    def infer_mime(cls, values):
        if values.get("mime_type") is not None:
            return values

        if values.get("url") is None:
            raise ValueError("If `url` is not used, `mime_type` must be specified.")

        suffix = values["url"].split(".")[-1]

        if suffix not in MIME_TYPES:
            raise ValueError(
                f"Unknown image mime type: {suffix}. Please specify `mime_type`."
            )

        values["mime_type"] = MIME_TYPES[suffix]

        return values

    @property
    def bytes(self):
        """The raw image bytes. Will make a network request if only `url` is specified and data has not been loaded yet."""
        if self.data:
            return self.data
        if self.url:
            self.data = load_image_bytes_from_url(self.url)
            return self.data
        raise ValueError("Cannot get bytes as image does not have a URL or data.")
