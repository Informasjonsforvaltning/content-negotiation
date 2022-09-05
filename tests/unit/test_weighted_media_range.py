"""Unit test cases for the content_negotiation function."""
import pytest

from content_negotiation.content_negotiation import (
    InvalidMediaRangeError,
    MediaRangeSpecificity,
    WeightedMediaRange,
)


@pytest.mark.unit
def test_initialization_default_q() -> None:
    """Should a WeightedMediaRange object with defalt value for q = 1.0."""
    media_range = "text/turtle"
    wmr = WeightedMediaRange(media_range)
    assert wmr
    assert wmr.q == 1.0
    assert wmr.specificity == MediaRangeSpecificity.SPECIFIC


@pytest.mark.unit
def test_initialization_given_q() -> None:
    """Should a WeightedMediaRange object."""
    media_range = "text/turtle;q=0.5"
    wmr = WeightedMediaRange(media_range)
    assert wmr
    assert wmr.q == 0.5
    assert wmr.specificity == MediaRangeSpecificity.SPECIFIC


@pytest.mark.unit
def test_initialization_invalid_media_range() -> None:
    """Should raise InvalidMediaRangeError a WeightedMediaRange object."""
    media_range = "text"
    with pytest.raises(InvalidMediaRangeError):
        WeightedMediaRange(media_range)


@pytest.mark.unit
def test_initialization_non_specific() -> None:
    """Should a WeightedMediaRange object with defalt value for q = 1.0."""
    media_range = "*/*"
    wmr = WeightedMediaRange(media_range)
    assert wmr
    assert wmr.q == 1.0
    assert wmr.specificity == MediaRangeSpecificity.NONSPECIFIC


@pytest.mark.unit
def test_initialization_sub_type_non_specific() -> None:
    """Should a WeightedMediaRange object with defalt value for q = 1.0."""
    media_range = "text/*"
    wmr = WeightedMediaRange(media_range)
    assert wmr
    assert wmr.q == 1.0
    assert wmr.specificity == MediaRangeSpecificity.SUBTYPE_INSPECIFIC


@pytest.mark.unit
def test_larger_than() -> None:
    """Should return True if self is larger than other."""
    media_range = "text/turtle;q=0.5"
    wmr = WeightedMediaRange(media_range)
    other = WeightedMediaRange("text/turtle;q=0.3")
    assert wmr > other


@pytest.mark.unit
def test_smaller_than() -> None:
    """Should return True if self is smaller than other."""
    media_range = "text/turtle;q=0.5"
    wmr = WeightedMediaRange(media_range)
    other = WeightedMediaRange("text/turtle;q=0.8")
    assert wmr < other


@pytest.mark.unit
def test_larger_than_when_different_types() -> None:
    """Should raise TypeError."""
    media_range = "text/turtle;q=0.5"
    wmr = WeightedMediaRange(media_range)
    other = "text/turtle;q=0.3"
    with pytest.raises(TypeError):
        wmr > other  # type: ignore  # noqa: B015

    with pytest.raises(TypeError):
        other > wmr  # noqa: B015


@pytest.mark.unit
def test_str() -> None:
    """Should return a string representation of the object."""
    media_range = "text/turtle;q=0.5"
    wmr = WeightedMediaRange(media_range)
    assert str(wmr) == "text/turtle;q=0.5"


@pytest.mark.unit
def test_media_range() -> None:
    """Should return the type, slash and sub-type."""
    media_range = "text/turtle;q=0.5"
    wmr = WeightedMediaRange(media_range)
    assert wmr.media_range() == "text/turtle"
