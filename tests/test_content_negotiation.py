"""Unit test cases for the content_negotiation function."""
from typing import List


from content_negotiation import decide_content_type

SUPPORTED_CONTENT_TYPES = [
    "text/turtle",
    "application/rdf+xml",
    "application/ld+json",
    "application/n-triples",
]


def test_content_negotiation() -> None:
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["text/turtle", "application/ld+json"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_2() -> None:
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["application/ld+json", "text/turtle"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_3() -> None:
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["not/acceptable", "*/*"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_4() -> None:
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["text/plain", "*/*"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_5() -> None:
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["*/*", "text/plain"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "text/turtle" == content_type
    ), f"For header-value '{accept_header}', content-type should be text/turtle."  # noqa: B950


def test_content_negotiation_6() -> None:
    """Should return 200 and correct content-type."""
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
    """Should return 200 and correct content-type."""
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
    """Should return 200 and correct content-type."""
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
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["application/ld+json;v=b3", "*/*"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_10() -> None:
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["*/*", "text/*", "application/ld+json"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/ld+json" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/ld+json."  # noqa: B950


def test_content_negotiation_11() -> None:
    """Should return 200 and correct content-type."""
    accept_header: List[str] = ["application/*", "text/turtle;q=0.2"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        "application/rdf+xml" == content_type
    ), f"For header-value '{accept_header}', content-type should be application/rdf+xml."  # noqa: B950


def test_content_negotiation_12() -> None:
    """Should return None."""
    accept_header: List[str] = ["text/"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert content_type is None, f"'{accept_header}' failed"


def test_content_negotiation_13() -> None:
    """Should return None."""
    accept_header: List[str] = ["text"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert content_type is None, f"'{accept_header}' failed"


def test_content_negotiation_14() -> None:
    """Should return None."""
    accept_header: List[str] = ["audio/*"]
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert content_type is None, f"'{accept_header}' failed"


def test_content_negotiation_no_supported_content_types() -> None:
    """Should return None."""
    accept_header: List[str] = ["*/*"]
    content_type = decide_content_type(accept_header, [])
    assert content_type is None, f"'{accept_header}' failed"


def test_content_negotiation_no_accept_header() -> None:
    """Should return default content-type."""
    accept_header: List[str] = []
    content_type = decide_content_type(accept_header, SUPPORTED_CONTENT_TYPES)
    assert (
        content_type is None
    ), f"For header-value '{accept_header}', content-type should be None."
