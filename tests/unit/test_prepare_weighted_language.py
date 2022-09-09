"""Unit test cases for the content_negotiation function."""
import pytest

from content_negotiation.language_negotiation import (
    prepare_weighted_languages,
)


@pytest.mark.unit
def test_prepare_weighted_languages_no_q_values() -> None:
    """Should return list with nb-NO first."""
    weighted_languages = ["nb-NO", "en-GB"]
    wl_sorted = prepare_weighted_languages(weighted_languages)
    assert len(wl_sorted) == 2
    assert wl_sorted[0].language == "nb-NO"
    assert wl_sorted[1].language == "en-GB"
    assert wl_sorted[0].q == 1.0
    assert wl_sorted[1].q == 1.0


@pytest.mark.unit
def test_prepare_weighted_languages_with_q() -> None:
    """Should return list with en-GB first."""
    weighted_languages = ["nb-NO;q=0.5", "en-GB"]
    wl_sorted = prepare_weighted_languages(weighted_languages)
    assert len(wl_sorted) == 2
    assert wl_sorted[0].language == "en-GB"
    assert wl_sorted[1].language == "nb-NO"
    assert wl_sorted[0].q == 1.0
    assert wl_sorted[1].q == 0.5


@pytest.mark.unit
def test_prepare_weighted_languages_with_q_and_subtype_inspecific() -> None:
    """Should return list en-GB first."""
    weighted_languages = ["nb-NO;q=0.5", "en-GB"]
    wl_sorted = prepare_weighted_languages(weighted_languages)
    assert len(wl_sorted) == 2
    assert wl_sorted[0].language == "en-GB"
    assert wl_sorted[1].language == "nb-NO"
    assert wl_sorted[0].q == 1.0
    assert wl_sorted[1].q == 0.5


@pytest.mark.unit
def test_prepare_weighted_languages_above_1_0() -> None:
    """Should return list with media range and q=1.0."""
    weighted_languages = ["nb-NO;q=1.1"]
    wl_sorted = prepare_weighted_languages(weighted_languages)
    assert len(wl_sorted) == 1
    assert wl_sorted[0].language == "nb-NO"
    assert wl_sorted[0].q == 1.0


@pytest.mark.unit
def test_prepare_weighted_languages_below_0_0() -> None:
    """Should return list without the given media range."""
    weighted_languages = ["nb-NO;q=-1.1"]
    wl_sorted = prepare_weighted_languages(weighted_languages)
    assert len(wl_sorted) == 1
    assert wl_sorted[0].language == "nb-NO"
    assert wl_sorted[0].q == 0.0


@pytest.mark.unit
def test_prepare_weighted_languages_equal_q_value() -> None:
    """Should return list without the first in first position."""
    weighted_languages = ["nb-NO;q=0.8", "en-GB;q=0.8"]
    wl_sorted = prepare_weighted_languages(weighted_languages)
    assert len(wl_sorted) == 2
    assert wl_sorted[0].language == "nb-NO"
    assert wl_sorted[0].q == 0.8
    assert wl_sorted[1].language == "en-GB"
    assert wl_sorted[1].q == 0.8
