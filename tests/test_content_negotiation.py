"""Unit test cases for the content_negotiation function."""
from typing import List

import pytest

from content_negotiation import decide_content_type, NoAgreeableContentTypeError

SUPPORTED_CONTENT_TYPES = [
    "text/turtle",
    "application/rdf+xml",
    "application/ld+json",
    "application/n-triples",
]


def test_content_negotiation() -> None:
    """Should return text/turtle."""
    accept_header: List[str] = ["text/turtle", "application/ld+json"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_2() -> None:
    """Should return application/ld+json."""
    accept_header: List[str] = ["application/ld+json", "text/turtle"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_3() -> None:
    """Should return text/turtle."""
    accept_header: List[str] = ["not/acceptable", "*/*"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_4() -> None:
    """Should return text/turtle."""
    accept_header: List[str] = ["text/plain", "*/*"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_5() -> None:
    """Should return text/turtle."""
    accept_header: List[str] = ["*/*", "text/plain"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_6() -> None:
    """Should return application/rdf+xml."""
    accept_header: List[str] = [
        "application/json",
        "application/*",
        "*/*",
    ]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/rdf+xml" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/rdf+xml."  # noqa: B950


def test_content_negotiation_7() -> None:
    """Should return applicaton/ld+json."""
    accept_header: List[str] = [
        "*/*;q=0.8",
        "text/plain",
        "application/signed-exchange;q=0.9",
        "application/ld+json",
    ]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_8() -> None:
    """Should return application/ld+json."""
    accept_header: List[str] = [
        "*/*;q=0.8;v=b3",
        "text/plain",
        "application/signed-exchange;v=b3;q=0.9",
        "application/ld+json",
    ]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_9() -> None:
    """Should return application/ld+json."""
    accept_header: List[str] = ["application/ld+json;v=b3", "*/*"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_10() -> None:
    """Should return application/ld+json."""
    accept_header: List[str] = ["*/*", "text/*", "application/ld+json"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_11() -> None:
    """Should return application/rdf+xml."""
    accept_header: List[str] = ["application/*", "text/turtle;q=0.2"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/rdf+xml" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/rdf+xml."  # noqa: B950


def test_content_negotiation_12() -> None:
    """Should raise NoAgreeableContentTypeError."""
    accept_header: List[str] = ["text/"]
    with pytest.raises(NoAgreeableContentTypeError):
        _ = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)


def test_content_negotiation_media_range_invalid() -> None:
    """Should raise NoAgreeableContentTypeError."""
    accept_header: List[str] = ["text"]
    with pytest.raises(NoAgreeableContentTypeError):
        _ = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)


def test_content_negotiation_14() -> None:
    """Should raise NoAgreeableContentTypeError."""
    accept_header: List[str] = ["audio/*"]
    with pytest.raises(NoAgreeableContentTypeError):
        _ = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)


def test_content_negotiation_no_supported_content_types() -> None:
    """Should raise NoAgreeableContentTypeError."""
    accept_header: List[str] = ["*/*"]
    with pytest.raises(NoAgreeableContentTypeError):
        _ = decide_content_type(accept_header, [])


def test_content_negotiation_no_accept_header() -> None:
    """Should return default content-type."""
    accept_header: List[str] = []
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_q_value_0_0() -> None:
    """Should be ignored and return default content-type."""
    accept_header: List[str] = ["application/json;q=0.0"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_q_value_below_0_0() -> None:
    """Should be ignored and return default content-type."""
    accept_header: List[str] = ["application/json;q=-1.0"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_header_contains_only_empty_string() -> None:
    """Should raise NoAgreeableContentTypeError."""
    accept_header: List[str] = [""]
    with pytest.raises(NoAgreeableContentTypeError):
        _ = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
