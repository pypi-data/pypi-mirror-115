"""Utilities to report client errors to Sentry (sentry.io).

See the Sentry docs for details.
"""
from typing import Optional

import sentry_sdk


# Only send events in production. Don't clutter Sentry with other events.
def _drop_non_prod_events(event, hint):  # pylint: disable=unused-argument
    if event["environment"] != "prod":
        return None
    return event


def set_up_sentry(environment: str, release: Optional[str]) -> None:
    if release is None:
        release = "unknown"
    # This Sentry DSN is not security sensitive.
    sentry_sdk.init(
        "https://478ff7ea710140e895b0c8734b9fb802@o923608.ingest.sentry.io/5871105",
        traces_sample_rate=1.0,
        release=release,
        environment=environment,
        before_send=_drop_non_prod_events,
    )


def set_user_for_sentry(user_id: str):
    """Associate the current Terality user ID to Sentry events."""
    sentry_sdk.set_user({"id": user_id})


def set_sentry_tags(numpy_version: str, pandas_version: str):
    # Sentry does send these versions as part of the event context, but settings them as tags
    # allows for searching issues by these versions (Sentry context is not searchable).
    sentry_sdk.set_tag("versions.numpy", numpy_version)
    sentry_sdk.set_tag("versions.pandas", pandas_version)
