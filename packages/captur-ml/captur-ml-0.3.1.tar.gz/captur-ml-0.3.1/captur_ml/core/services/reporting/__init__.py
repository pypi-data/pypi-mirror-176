import os
import sentry_sdk

from google.cloud import error_reporting
from captur_ml.core.exceptions import SentryDSNNotProvidedError
from sentry_sdk.integrations.gcp import GcpIntegration


def get_google_cloud_error_reporting_client() -> error_reporting.Client:
    """Returns a Google Cloud error reporting client

    Returns:
        error_reporting.Client: A Google Cloud error reporting client
    """
    return error_reporting.Client()


def initialise_sentry(environment="development", gcp_integration=False):
    """Initialises the Sentry client according to the SENTRY_DSN environment variable

    Raises:
        `captur_ml.core.exceptions.SentryDSNNotProvidedError`: If the SENTRY_DSN environment variable is not set
    """
    if not os.getenv("SENTRY_DSN"):
        raise SentryDSNNotProvidedError(
            "SENTRY_DSN environment variable must be set to use Sentry for error reporting."
        )

    if gcp_integration:
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            environment=environment,
            integrations=[GcpIntegration(timeout_warning=True)],
            traces_sample_rate=1.0,
        )
    else:
        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"), environment=environment, traces_sample_rate=1.0
        )
