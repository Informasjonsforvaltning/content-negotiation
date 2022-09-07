"""Datacatalog package.

Modules:
    resource
    dataset
    dataset_series
    catalog
    dataservice
    distribution
"""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .content_negotiation import decide_content_type, NoAgreeableContentTypeError
from .language_negotiation import decide_language, NoAgreeableLanguageError
