"""Package for function determining content-type based on accept header.

Example:
    >>> from content_negotiation import decide_content_type
    >>>
    >>> accept = ["application/json", "text/html", "text/plain, "text/*;q=0.8"]
    >>> supported = ["text/turtle", "application/json"]
    >>> decide_content_type(accept, supported)
    'application/json'
"""
from enum import Enum
import logging
from typing import Any, List, Optional


class InvalidMediaRangeError(ValueError):
    """Exception for invalid media ranges."""

    pass


class NoAgreeableContentTypeError(Exception):
    """Exception for no agreeable content type."""

    pass


class MediaRangeSpecificity(Enum):
    """Enum for media range specificity."""

    NONSPECIFIC = 0
    SUBTYPE_INSPECIFIC = 1
    SPECIFIC = 2


class WeightedMediaRange:
    """Class for handling weighted media ranges."""

    type: str
    sub_type: str
    q: float = 1.0
    specificity: MediaRangeSpecificity

    def __init__(self, media_range: str) -> None:
        """Initialize the weighted media range."""
        weighted_media_range_split = media_range.split(";")
        # Instantiate weighted media range:
        try:
            logging.debug(
                f"Assigning q-parameter for weighted media range: {media_range}"
            )
            self.type, self.sub_type = weighted_media_range_split[0].split("/")
            # Check if media range is specific:
            if self.type == "*":
                self.specificity = MediaRangeSpecificity.NONSPECIFIC
            elif self.sub_type == "*":
                self.specificity = MediaRangeSpecificity.SUBTYPE_INSPECIFIC
            else:
                self.specificity = MediaRangeSpecificity.SPECIFIC

            # If q-parameter is present, assign it:
            for weighted_media_range_part in weighted_media_range_split[1:]:
                if weighted_media_range_part.startswith("q="):
                    self.q = float(
                        # RFC specifies only 3 decimals may be used in q value.
                        # Must strip additional decimals so that q bonus from specificity
                        # results in correct sorting.
                        weighted_media_range_part.split("=")[1][0:5]
                    )
        except ValueError as e:
            raise InvalidMediaRangeError(f"Invalid media range: {media_range}") from e

    def __eq__(self, other: Any) -> bool:
        """Compare two weighted media ranges."""
        if isinstance(other, str):
            return f"{self.type}/{self.sub_type}" == other
        return False  # pragma: no cover

    def __lt__(self, other: Any) -> bool:
        """Compare two weighted media ranges."""
        if isinstance(other, WeightedMediaRange):
            # If weighted media ranges are equal, compare specificity:
            if self.q == other.q:
                return self.specificity.value < other.specificity.value
            # If weighted media ranges are not equal, compare q value:
            return self.q < other.q
        raise TypeError(
            f"Cannot compare WeightedMediaRange with {type(other).__name__}"
        )

    def __str__(self) -> str:
        """Return the weighted media range as a string."""
        return f"{self.type}/{self.sub_type};q={self.q}"

    def media_range(self) -> str:
        """Return the media range."""
        return f"{self.type}/{self.sub_type}"


def prepare_weighted_media_ranges(
    weighted_media_ranges: List[str],
) -> List[WeightedMediaRange]:
    """Prepare the accept weighted media ranges and sort on q-parameter."""
    logging.debug(f"Preparing accept weighted media ranges: {weighted_media_ranges}")
    # Assign q-parameter:
    weighted_media_ranges_sorted: List[WeightedMediaRange] = []

    for accept_weighted_media_range in weighted_media_ranges:
        # Instantiate weighted media range:
        try:
            weighted_media_range = WeightedMediaRange(accept_weighted_media_range)

            weighted_media_ranges_sorted.append(weighted_media_range)
        except InvalidMediaRangeError:
            logging.debug(
                "Ignoring invalid weighted media range: %s", accept_weighted_media_range
            )
            pass  # ignore invalid media range

    # Sort and return list of weighted media ranges:
    weighted_media_ranges_sorted.sort(reverse=True)
    logging.debug(
        f"Accept weighted media ranges sorted: {', '.join(str(p) for p in weighted_media_ranges_sorted)}"  # noqa: B950
    )
    return weighted_media_ranges_sorted


def get_default_content_type(
    supported_content_types: List[str], type: Optional[str] = None
) -> str:
    """Return the default content type."""
    if type is None:
        return supported_content_types[0]

    return next(
        media_type
        for media_type in supported_content_types
        if type == media_type.split("/")[0]
    )


def is_media_range_type_in_supported_content_types(
    media_range_type: str, supported_content_types: List[str]
) -> bool:
    """Return True if media range type is in supported content types."""
    return any(
        media_range_type == media_type.split("/")[0]
        for media_type in supported_content_types
    )


def decide_content_type(
    accept_headers: List[str], supported_content_types: List[str]
) -> str:
    """Decide the content type based on the given accept-header and supported content-types.

    Args:
        accept_headers (List[str]): the accept headers.
        supported_content_types (List[str]): List of supported content types.

    Returns:
        The content type of the response.

    Raises:
        NoAgreeableContentTypeError: If no agreeable content type is found.

    """
    logging.debug(
        f"Deciding content types {accept_headers} " f"against {supported_content_types}"
    )
    # Checking a couple of corner cases:
    if len(supported_content_types) == 0 or len(accept_headers) == 0:
        raise NoAgreeableContentTypeError(
            "No supported content types or accept headers provided."
        )

    weighted_media_ranges: List[str] = (
        ",".join(accept_headers).replace(" ", "").split(",")
    )
    weighted_media_ranges_sorted = prepare_weighted_media_ranges(weighted_media_ranges)

    for weighted_media_range in weighted_media_ranges_sorted:
        logging.debug(f"Checking weighted media range: {weighted_media_range}")
        if weighted_media_range in supported_content_types:
            return weighted_media_range.media_range()
        elif weighted_media_range.type == "*" and weighted_media_range.sub_type == "*":
            return get_default_content_type(supported_content_types)
        else:
            # Assumes valid mimetypes from `prepare_mime_types`
            if (
                weighted_media_range.sub_type == "*"
                and is_media_range_type_in_supported_content_types(
                    weighted_media_range.type,
                    supported_content_types,
                )
            ):
                return get_default_content_type(
                    supported_content_types, type=weighted_media_range.type
                )
    raise NoAgreeableContentTypeError("No agreeable content type found.")
