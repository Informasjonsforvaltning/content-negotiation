"""Unit test cases for the content_negotiation function."""
from typing import List

import pytest

from content_negotiation.content_negotiation import (
    is_media_range_type_in_supported_content_types,
)


@pytest.mark.unit
def test_is_media_range_type_in_supported_content_types_type_supported() -> None:
    """Should return True."""
    media_range_type = "text"
    supported_content_types: List[str] = ["text/turtle", "application/ld+json"]
    assert (
        is_media_range_type_in_supported_content_types(
            media_range_type, supported_content_types
        )
        is True
    )


@pytest.mark.unit
def test_is_media_range_type_in_supported_content_types_type_not_supported() -> None:
    """Should return False."""
    media_range_type = "text"
    supported_content_types: List[str] = ["application/rdf+xml", "application/ld+json"]
    assert (
        is_media_range_type_in_supported_content_types(
            media_range_type, supported_content_types
        )
        is False
    )


@pytest.mark.unit
def test_is_media_range_type_in_supported_content_types_supported_empty() -> None:
    """Should return False."""
    media_range_type = "text"
    supported_content_types: List[str] = []
    assert (
        is_media_range_type_in_supported_content_types(
            media_range_type, supported_content_types
        )
        is False
    )
