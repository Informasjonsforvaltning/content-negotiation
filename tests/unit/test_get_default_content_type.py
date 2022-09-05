"""Unit test cases for the content_negotiation function."""
import pytest

from content_negotiation.content_negotiation import get_default_content_type


@pytest.mark.unit
def test_get_default_content_type_no_type() -> None:
    """Should return first content type in supported_content_types."""
    supported_content_types = ["text/turtle", "application/ld+json"]
    assert (
        get_default_content_type(supported_content_types=supported_content_types)
        == supported_content_types[0]
    )


@pytest.mark.unit
def test_get_default_content_type_given_type() -> None:
    """Should return the first content type of given type."""
    supported_content_types = ["text/turtle", "application/ld+json"]
    type = "application"
    assert (
        get_default_content_type(
            supported_content_types=supported_content_types, type=type
        )
        == supported_content_types[1]
    )
