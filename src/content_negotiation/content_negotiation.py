"""Package for function determining content-type based on accept header.

Example:
    >>> from content_negotiation import decide_content_type
    >>>
    >>> accept = ["application/json", "text/html", "text/plain"]
    >>> supported = ["text/turtle;q=0.9", "application/json"]
    >>> decide_content_type(accept, supported)
    'application/json'
"""
import logging
from typing import Any, List, Optional


class InvalidMediaRangeError(ValueError):
    """Exception for invalid media ranges."""

    pass


class WeightedMediaRange:
    """Class for handling weighted media ranges."""

    type: str
    sub_type: str
    q: float = 1.0

    def __init__(self, media_range: str) -> None:
        """Initialize the weighted media range."""
        weighted_media_range_split = media_range.split(";")
        # Instantiate weighted media range:
        try:
            logging.debug(
                f"Assigning q-parameter for weighted media range: {media_range}"
            )
            self.type, self.sub_type = weighted_media_range_split[0].split("/")
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

    def __eq__(self, other: Any) -> bool:  # pragma: no cover
        """Compare two weighted media ranges."""
        if isinstance(other, str):
            return f"{self.type}/{self.sub_type}" == other
        if isinstance(other, WeightedMediaRange):
            return self.type == other.type and self.sub_type == other.sub_type
        return False

    def __str__(self) -> str:
        """Return the weighted media range as a string."""
        return f"{self.type}/{self.sub_type};q={self.q}"

    def media_range(self) -> str:
        """Return the media range."""
        return f"{self.type}/{self.sub_type}"


def prepare_weighted_media_ranges(
    accept_weighted_media_ranges: List[str],
) -> List[WeightedMediaRange]:
    """Prepare the accept weighted media ranges and sort on q-parameter."""
    logging.debug(
        f"Preparing accept weighted media ranges: {accept_weighted_media_ranges}"
    )
    # Assign q-parameter:
    accept_weighted_media_ranges_sorted: List[WeightedMediaRange] = []

    for accept_weighted_media_range in accept_weighted_media_ranges:
        # Instantiate weighted media range:
        try:
            weighted_media_range = WeightedMediaRange(accept_weighted_media_range)

            accept_weighted_media_ranges_sorted.append(weighted_media_range)
        except InvalidMediaRangeError:
            logging.debug(
                "Ignoring invalid weighted media range: %s", accept_weighted_media_range
            )
            pass  # ignore invalid media range

    # Adjust q-parameters with regard to specificity:
    # Highest q-parameter is the most specific:
    for weighted_media_range in accept_weighted_media_ranges_sorted:
        logging.debug(
            f"Ajusting q-parameter for weighted media range: {weighted_media_range}"
        )
        if weighted_media_range.type == "*":
            pass
        elif weighted_media_range.sub_type == "*":
            weighted_media_range.q = weighted_media_range.q + 0.0001
        else:
            weighted_media_range.q = weighted_media_range.q + 0.0002

    # Sort on q-parameter and return list of weighted media ranges:
    accept_weighted_media_ranges_sorted.sort(key=lambda x: x.q, reverse=True)
    logging.debug(
        f"Accept weighted media ranges sorted: {', '.join(str(p) for p in accept_weighted_media_ranges_sorted)}"  # noqa: B950
    )
    return accept_weighted_media_ranges_sorted


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
    accept_weighted_media_ranges: List[str], supported_content_types: List[str]
) -> Optional[str]:
    """Decide the content type of the response.

    Args:
        accept_weighted_media_ranges (List[str]): List of weighted media ranges from the accept header. # noqa: B950
        supported_content_types (List[str]): List of supported content types.

    Returns:
        The content type of the response.

    """
    logging.debug(
        f"Deciding content types {accept_weighted_media_ranges} "
        f"against {supported_content_types}"
    )
    # Checking a couple of corner cases:
    if len(supported_content_types) == 0 or len(accept_weighted_media_ranges) == 0:
        return None

    content_type: Optional[str] = None
    accept_weighted_media_ranges_sorted = prepare_weighted_media_ranges(
        accept_weighted_media_ranges
    )
    for weighted_media_range in accept_weighted_media_ranges_sorted:
        logging.debug(f"Checking weighted media range: {weighted_media_range}")
        if weighted_media_range in supported_content_types:
            content_type = weighted_media_range.media_range()
            break
        elif weighted_media_range.type == "*" and weighted_media_range.sub_type == "*":
            content_type = get_default_content_type(supported_content_types)
            break
        else:
            # Assumes valid mimetypes from `prepare_mime_types`
            if (
                weighted_media_range.sub_type == "*"
                and is_media_range_type_in_supported_content_types(
                    weighted_media_range.type,
                    supported_content_types,
                )
            ):
                content_type = get_default_content_type(
                    supported_content_types, type=weighted_media_range.type
                )
                break
            else:
                content_type = None
    return content_type
