"""Unit test cases for the content_negotiation function."""
from typing import List

import pytest

from content_negotiation import decide_language
from content_negotiation.language_negotiation import NoAgreeableLanguageError

SUPPORTED_LANGUAGES = ["en-GB", "en", "nb-NO", "nb", "en-US"]


def test_language_negotiation_accept_header_contains_one_supported_language() -> None:
    """Should return the supported language."""
    accept_language_header: List[str] = ["en-GB"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        "en-GB" == content_language
    ), f"For header-value '{accept_language_header}', content-language should be en-GB."  # noqa: B950


def test_language_negotiation_accept_header_contains_two_supported_languages() -> None:
    """Should return the first supported language."""
    accept_language_header: List[str] = ["en-GB", "nb-NO"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        "en-GB" == content_language
    ), f"For header-value '{accept_language_header}', content-language should be en-GB."  # noqa: B950


def test_language_negotiation_accept_header_contains_languages_with_q_factor() -> None:
    """Should return the language with highest q-factor."""
    accept_language_header: List[str] = ["en-GB;q=0.8", "nb-NO;q=0.9"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        "nb-NO" == content_language
    ), f"For header-value '{accept_language_header}', content-language should be nb-NO."  # noqa: B950


def test_language_negotiation_accept_header_contains_no_supported_languages() -> None:
    """Should raise NoAgreeableLanguageError."""
    accept_language_header: List[str] = ["da", "no"]
    with pytest.raises(NoAgreeableLanguageError):
        decide_language(accept_language_header, SUPPORTED_LANGUAGES)


def test_language_negotiation_accept_header_contains_no_languages() -> None:
    """Should return the default language."""
    accept_language_header: List[str] = []
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        SUPPORTED_LANGUAGES[0] == content_language
    ), f"For header-value '{accept_language_header}', content-language should be en-GB."  # noqa: B950


def test_language_negotiation_accept_header_contains_languages_and_no_supported_language() -> None:  # noqa: B950
    """Should raise NoAgreeableLanguageError."""
    accept_language_header: List[str] = ["en-GB", "nb-NO"]
    supported_languages: List[str] = []
    with pytest.raises(NoAgreeableLanguageError):
        decide_language(accept_language_header, supported_languages)
