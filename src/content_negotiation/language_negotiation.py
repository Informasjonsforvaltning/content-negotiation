"""Module for determining content-language based on accept-language header.

Example:
    >>> from content_negotiation import decide_language, NoAgreeableLanguageError
    >>>
    >>> accept_language_headers = ["en-GB;q=0.8", "nb-NO;q=0.9"]
    >>> supported_languages = ["en-GB", "en", "nb-NO", "nb", "en-US"]
    >>>
    >>> try:
    >>>     content_language = decide_language(accept_language_headers, supported_languages)
    >>> except NoAgreeableLanguageError:
    >>>     print("No agreeable language found.")
    >>>     # Handle error, by returning e.g. 406 Not Acceptable
    >>> print(content_language)
    'nb-NO'
"""
import logging
from typing import Any, List


class NoAgreeableLanguageError(Exception):
    """Exception for no agreeable language."""

    pass


class WeightedLanguage:
    """Class for handling weighted languages."""

    language: str
    q: float = 1.0

    def __init__(self, language: str) -> None:
        """Initialize the weighted language."""
        weighted_language_split = language.split(";")
        # Instantiate weighted language:
        logging.debug(f"Assigning q-parameter for weighted languag: {language}")
        self.language = weighted_language_split[0]

        # If q-parameter is present, assign it:
        for weighted_language_part in weighted_language_split[1:]:
            if weighted_language_part.startswith("q="):
                self.q = float(
                    # RFC specifies only 3 decimals may be used in q value.
                    weighted_language_part.split("=")[1][0:5]
                )

    def __eq__(self, other: Any) -> bool:
        """Compare two weighted languages."""
        if isinstance(other, str):
            return self.language == other
        return False  # pragma: no cover

    def __lt__(self, other: Any) -> bool:
        """Compare two weighted languages."""
        if isinstance(other, WeightedLanguage):
            # If weighted languages are not equal, compare q value:
            return self.q < other.q
        raise TypeError(
            f"Cannot compare WeightedLanguage with {type(other).__name__}"
        )  # pragma: no cover

    def __str__(self) -> str:
        """Return the weighted language as a string."""
        return f"{self.language};q={self.q}"


def prepare_weighted_languages(
    weighted_languages: List[str],
) -> List[WeightedLanguage]:
    """Prepare the accept weighted languages and sort on q-parameter."""
    logging.debug(f"Preparing accept weighted languages: {weighted_languages}")
    # Assign q-parameter:
    weighted_languages_sorted: List[WeightedLanguage] = []

    for accept_weighted_language in weighted_languages:
        # Instantiate weighted language:
        weighted_language = WeightedLanguage(accept_weighted_language)
        weighted_languages_sorted.append(weighted_language)

    # Sort and return list of weighted languages:
    weighted_languages_sorted.sort(reverse=True)
    logging.debug(
        f"Accept weighted languages sorted: {', '.join(str(p) for p in weighted_languages_sorted)}"  # noqa: B950
    )
    return weighted_languages_sorted


def get_default_language(supported_languages: List[str]) -> str:
    """Get the default language.

    Args:
        supported_languages (List[str]): List of supported languages.

    Returns:
        The default language.

    """
    # If no accept-language header is provided, return the first supported language:
    logging.debug(
        "No accept-language header provided. Returning first supported language."
    )
    return supported_languages[0]


def decide_language(
    accept_language_headers: List[str], supported_languages: List[str]
) -> str:
    """Decide the language based on the given accept-language header and supported languages.

    Args:
        accept_language_headers (List[str]): the accept-langugage headers.
        supported_languages (List[str]): List of supported languages.

    Returns:
        The content language of the response.

    Raises:
        NoAgreeableLanguageError: If no agreeable language is found.

    """
    logging.debug(
        f"Deciding languages {accept_language_headers} "
        f"against {supported_languages}"
    )
    # Checking a couple of corner cases:
    if len(supported_languages) == 0:
        raise NoAgreeableLanguageError(
            "No supported languages or accept language headers provided."
        )
    if len(accept_language_headers) == 0:
        return get_default_language(supported_languages)

    weighted_languages: List[str] = (
        ",".join(accept_language_headers).replace(" ", "").split(",")
    )
    weighted_languages_sorted = prepare_weighted_languages(weighted_languages)

    for weighted_language in weighted_languages_sorted:
        logging.debug(f"Checking weighted language: {weighted_language}")
        if weighted_language in supported_languages:
            return weighted_language.language

    raise NoAgreeableLanguageError("No agreeable language found.")
