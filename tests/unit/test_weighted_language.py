"""Unit test cases for the content_negotiation function."""
import pytest

from content_negotiation.language_negotiation import (
    WeightedLanguage,
)


@pytest.mark.unit
def test_initialization_default_q() -> None:
    """Should a WeightedLanguage object with defalt value for q = 1.0."""
    language = "nb-NO"
    wl = WeightedLanguage(language)
    assert wl
    assert wl.q == 1.0


@pytest.mark.unit
def test_initialization_given_q() -> None:
    """Should a WeightedLanguage object."""
    language = "nb-NO;q=0.5"
    wl = WeightedLanguage(language)
    assert wl
    assert wl.q == 0.5


@pytest.mark.unit
def test_initialization_q_above_1_0() -> None:
    """Should return a WeightedLanguage object with q = 1.0."""
    language = "nb-NO;q=1.1"
    wl = WeightedLanguage(language)
    assert wl
    assert wl.q == 1.0


@pytest.mark.unit
def test_initialization_q_below_0_0() -> None:
    """Should a WeightedLanguage object with q = 0.0."""
    language = "nb-NO;q=-1.1"
    wl = WeightedLanguage(language)
    assert wl
    assert wl.q == 0.0


@pytest.mark.unit
def test_larger_than() -> None:
    """Should return True if self is larger than other."""
    language = "nb-NO;q=0.5"
    wl = WeightedLanguage(language)
    other = WeightedLanguage("nb-NO;q=0.3")
    assert wl > other


@pytest.mark.unit
def test_smaller_than() -> None:
    """Should return True if self is smaller than other."""
    language = "nb-NO;q=0.5"
    wl = WeightedLanguage(language)
    other = WeightedLanguage("nb-NO;q=0.8")
    assert wl < other


@pytest.mark.unit
def test_larger_than_when_different_types() -> None:
    """Should raise TypeError."""
    language = "nb-NO;q=0.5"
    wl = WeightedLanguage(language)
    other = "nb-NO;q=0.3"
    with pytest.raises(TypeError):
        wl > other  # type: ignore  # noqa: B015

    with pytest.raises(TypeError):
        other > wl  # noqa: B015


@pytest.mark.unit
def test_str() -> None:
    """Should return a string representation of the object."""
    language = "nb-NO;q=0.5"
    wl = WeightedLanguage(language)
    assert str(wl) == "nb-NO;q=0.5"


@pytest.mark.unit
def test_language() -> None:
    """Should return the type, slash and sub-type."""
    language = "nb-NO;q=0.5"
    wl = WeightedLanguage(language)
    assert wl.language == "nb-NO"
