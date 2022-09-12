"""Unit test cases for the content_negotiation function."""
from typing import List

import pytest

from content_negotiation import decide_language
from content_negotiation.language_negotiation import NoAgreeableLanguageError

SUPPORTED_LANGUAGES = ["en-GB", "en", "nb-NO", "nb", "en-US"]


def test_language_negotiation_accept_language_header_contains_one_supported_language() -> None:
    """Should return the supported language."""
    accept_language_header: List[str] = ["en-GB"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        "en-GB" == content_language
    ), f"For header-value '{accept_language_header}', content-language should be en-GB."  # noqa: B950


def test_language_negotiation_accept_language_header_contains_two_supported_languages() -> None:
    """Should return the first supported language."""
    accept_language_header: List[str] = ["en-GB", "nb-NO"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        "en-GB" == content_language
    ), f"For header-value '{accept_language_header}', content-language should be en-GB."  # noqa: B950


def test_language_negotiation_accept_language_header_contains_languages_with_q_factor() -> None:
    """Should return the language with highest q-factor."""
    accept_language_header: List[str] = ["en-GB;q=0.8", "nb-NO;q=0.9"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        "nb-NO" == content_language
    ), f"For header-value '{accept_language_header}', content-language should be nb-NO."  # noqa: B950


def test_language_negotiation_accept_language_header_contains_no_supported_languages() -> None:
    """Should raise NoAgreeableLanguageError."""
    accept_language_header: List[str] = ["da", "no"]
    with pytest.raises(NoAgreeableLanguageError):
        decide_language(accept_language_header, SUPPORTED_LANGUAGES)


def test_language_negotiation__q_value_0_0() -> None:
    """Should return the default language."""
    accept_language_header: List[str] = ["nb-NO;q=0.0"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        SUPPORTED_LANGUAGES[0] == content_language  # en-GB
    ), f"For header-value '{accept_language_header}', content-language should be {SUPPORTED_LANGUAGES[0]}."  # noqa: B950


def test_language_negotiation__q_value_below_0_0() -> None:
    """Should be ignored and the default language returned."""
    accept_language_header: List[str] = ["nb-NO;q=-1.0"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        SUPPORTED_LANGUAGES[0] == content_language  # en-GB
    ), f"For header-value '{accept_language_header}', content-language should be {SUPPORTED_LANGUAGES[0]}."  # noqa: B950


def test_language_negotiation_accept_language_header_contains_languages_and_no_supported_language() -> None:  # noqa: B950
    """Should raise NoAgreeableLanguageError."""
    accept_language_header: List[str] = ["en-GB", "nb-NO"]
    supported_languages: List[str] = []
    with pytest.raises(NoAgreeableLanguageError):
        decide_language(accept_language_header, supported_languages)


def test_language_negotiation_accept_language_header_contains_only_semicolon_and_q() -> None:  # noqa: B950
    """Should raise NoAgreeableLanguageError."""
    accept_language_header: List[str] = [";q=0.8"]
    with pytest.raises(NoAgreeableLanguageError):
        decide_language(accept_language_header, SUPPORTED_LANGUAGES)


def test_language_negotiation_accept_language_header_contains_only_star() -> None:
    """Should return the default language."""
    accept_language_header: List[str] = ["*"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        SUPPORTED_LANGUAGES[0] == content_language  # "en-GB"
    ), f"For header-value '{accept_language_header}', content-language should be {SUPPORTED_LANGUAGES[0]}."  # noqa: B950


def test_language_negotiation_accept_language_header_contains_star_with_highest_q() -> None:
    """Should return the default language."""
    accept_language_header: List[str] = ["nb-NO;q=0.8,*;q=0.9"]
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        SUPPORTED_LANGUAGES[0] == content_language  # "en-GB"
    ), f"For header-value '{accept_language_header}', content-language should be {SUPPORTED_LANGUAGES[0]}."  # noqa: B950


def test_language_negotiation_accept_language_header_empty() -> None:
    """Should return the default language."""
    accept_language_header: List[str] = []
    content_language = decide_language(accept_language_header, SUPPORTED_LANGUAGES)
    assert (
        SUPPORTED_LANGUAGES[0] == content_language  # "en-GB"
    ), f"For header-value '{accept_language_header}', content-language should be {SUPPORTED_LANGUAGES[0]}."  # noqa: B950


def test_language_negotiation_accept_language_header_contains_only_empty_string() -> None:
    """Should raise NoAgreeableLanguageError."""
    accept_language_header: List[str] = [""]
    with pytest.raises(NoAgreeableLanguageError):
        decide_language(accept_language_header, SUPPORTED_LANGUAGES)
