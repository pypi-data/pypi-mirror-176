import regex


def is_storage_gs_uri(uri: str) -> bool:
    """
    Check if the given uri is a gs:// URI.

    Args:
        uri (str): The URI to check.

    Returns:
        bool: True if the URI is a valid Google Storage URI, False otherwise.
    """
    return regex.search(r"^gs://[a-z0-9][a-z0-9_-]{1,61}[a-z0-9]", uri) is not None


def is_storage_http_uri(uri) -> bool:
    """
    Check if the given uri is a storage.googleapis.com URI.

    Args:
        uri (str): The URI to check.

    Returns:
        bool: True if the URI is a valid Google Storage http URI, False otherwise.
    """
    return regex.search(r"^http[s]?://storage.googleapis.com", uri) is not None


def is_storage_appspot_uri(uri: str) -> bool:
    """
    Checks if the given uri is an appspot.com URI.
    Args:
        uri (str): The URI to check.

    Returns:
        bool: True if the URI is a valid appspot Google Storage URI, False otherwise.
    """
    return (
        regex.search(r"^http[s]?://.+.appspot.com.storage.googleapis.com", uri)
        is not None
    )


def get_gs_uri_from_uri(uri: str, appspot_name: str = "capturpwa") -> str:
    """Turns any Google Cloud Storage URL into a gs:// URI.

    Args:
        uri (str): The URI to convert.
        appspot_name (str, optional): The name of the appspot domain. Defaults to "capturpwa".

    Returns:
        str: The gs:// URI.

    Raises:
        ValueError: If the URL is not a valid GCS URL.
    """
    if is_storage_gs_uri(uri):
        return uri
    elif is_storage_http_uri(uri):
        return regex.sub(r"^http[s]?://storage.googleapis.com/*", "gs://", uri)
    elif is_storage_appspot_uri(uri):
        return regex.sub(
            r"^http[s]?://.+.appspot.com.storage.googleapis.com",
            f"gs://{appspot_name}.appspot.com",
            uri,
        )

    raise ValueError("Image URL is not a Google Cloud Storage URL.")


def get_bucket_from_gs_uri(gs_uri) -> str:
    """Extracts the Bucket name.

    Returns:
        str: Google Storage Bucket.
    """
    assert is_storage_gs_uri(gs_uri), "Not a valid Google Storage URI."

    exp = regex.search(r"^gs:\/\/([a-z0-9][a-z0-9_-]{1,61}[a-z0-9])", gs_uri)

    return None if exp is None else exp.group(1)


def get_filepath_from_gs_uri(gs_uri) -> str:
    """Extracts the filepath after the Bucket name.

    Returns:
        str: Filepath of the Google Storage URI.
    """
    assert is_storage_gs_uri(gs_uri), "Not a valid Google Storage URI."

    exp = regex.search(r"(?<=gs:\/\/[a-z0-9][a-z0-9_-]{1,61}[a-z0-9]\/).*", gs_uri)

    return None if exp is None else exp.group(0)
