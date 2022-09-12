"""Unit test cases for the content_negotiation function."""
import pytest

from content_negotiation.content_negotiation import (
    MediaRangeSpecificity,
    prepare_weighted_media_ranges,
)


@pytest.mark.unit
def test_prepare_weighted_media_ranges() -> None:
    """Should return list with text/turtle first."""
    weighted_media_ranges = ["text/turtle", "application/ld+json"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 2
    assert wmr_sorted[0].type == "text"
    assert wmr_sorted[0].sub_type == "turtle"
    assert wmr_sorted[1].type == "application"
    assert wmr_sorted[1].sub_type == "ld+json"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[1].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[0].q == 1.0
    assert wmr_sorted[1].q == 1.0


@pytest.mark.unit
def test_prepare_weighted_media_ranges_with_q() -> None:
    """Should return list with application/ld+json first."""
    weighted_media_ranges = ["text/turtle;q=0.5", "application/ld+json"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 2
    assert wmr_sorted[0].type == "application"
    assert wmr_sorted[0].sub_type == "ld+json"
    assert wmr_sorted[1].type == "text"
    assert wmr_sorted[1].sub_type == "turtle"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[1].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[0].q == 1.0
    assert wmr_sorted[1].q == 0.5


@pytest.mark.unit
def test_prepare_weighted_media_ranges_with_q_and_subtype_inspecific() -> None:
    """Should return list application/ld+json first."""
    weighted_media_ranges = ["text/*;q=0.5", "application/ld+json"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 2
    assert wmr_sorted[0].type == "application"
    assert wmr_sorted[0].sub_type == "ld+json"
    assert wmr_sorted[1].type == "text"
    assert wmr_sorted[1].sub_type == "*"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[1].specificity == MediaRangeSpecificity.SUBTYPE_INSPECIFIC
    assert wmr_sorted[0].q == 1.0
    assert wmr_sorted[1].q == 0.5


@pytest.mark.unit
def test_prepare_weighted_media_ranges_with_q_and_non_specific() -> None:
    """Should return list with application/ld+json first."""
    weighted_media_ranges = ["*/*;q=0.5", "application/ld+json"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 2
    assert wmr_sorted[0].type == "application"
    assert wmr_sorted[0].sub_type == "ld+json"
    assert wmr_sorted[1].type == "*"
    assert wmr_sorted[1].sub_type == "*"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[1].specificity == MediaRangeSpecificity.NONSPECIFIC
    assert wmr_sorted[0].q == 1.0
    assert wmr_sorted[1].q == 0.5


@pytest.mark.unit
def test_prepare_weighted_media_ranges_non_specific_and_subtype_inspecific() -> None:
    """Should return list application/* first."""
    weighted_media_ranges = ["*/*", "application/*"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 2
    assert wmr_sorted[0].type == "application"
    assert wmr_sorted[0].sub_type == "*"
    assert wmr_sorted[1].type == "*"
    assert wmr_sorted[1].sub_type == "*"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SUBTYPE_INSPECIFIC
    assert wmr_sorted[1].specificity == MediaRangeSpecificity.NONSPECIFIC
    assert wmr_sorted[0].q == 1.0
    assert wmr_sorted[1].q == 1.0


@pytest.mark.unit
def test_prepare_weighted_media_range_above_1_0() -> None:
    """Should return list with media range and q=1.0."""
    weighted_media_ranges = ["text/turtle;q=1.1"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 1
    assert wmr_sorted[0].type == "text"
    assert wmr_sorted[0].sub_type == "turtle"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[0].q == 1.0


@pytest.mark.unit
def test_prepare_weighted_media_range_below_0_0() -> None:
    """Should return list with media ranges and q=1.0 for the given media range."""
    weighted_media_ranges = ["text/turtle", "application/ld+json;q=-0.1"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 2
    assert wmr_sorted[0].type == "text"
    assert wmr_sorted[0].sub_type == "turtle"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[0].q == 1.0
    assert wmr_sorted[1].type == "application"
    assert wmr_sorted[1].sub_type == "ld+json"
    assert wmr_sorted[1].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[1].q == 0.0


@pytest.mark.unit
def test_prepare_weighted_media_ranges_equal_q_value() -> None:
    """Should return list without the first in first position."""
    weighted_media_ranges = ["text/turtle;q=0.8", "application/ld+json;q=0.8"]
    wmr_sorted = prepare_weighted_media_ranges(weighted_media_ranges)
    assert len(wmr_sorted) == 2
    assert wmr_sorted[0].type == "text"
    assert wmr_sorted[0].sub_type == "turtle"
    assert wmr_sorted[0].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[0].q == 0.8
    assert wmr_sorted[1].type == "application"
    assert wmr_sorted[1].sub_type == "ld+json"
    assert wmr_sorted[1].specificity == MediaRangeSpecificity.SPECIFIC
    assert wmr_sorted[1].q == 0.8
