"""Utils."""

import logging
from typing import Callable, List, Type, TypeVar

SortableItemType = TypeVar("SortableItemType")
ExceptionType = TypeVar("ExceptionType", bound=Exception)


class MustParseWithoutException(Exception):
    """Specifies that no exceptions should be ignored."""

    pass


def parse_and_sort_items(
    items: List[str],
    parse: Callable[[str], SortableItemType],
    ignore_exception: Type[ExceptionType],
) -> List[SortableItemType]:
    """Parse and sort header items."""
    logging.debug(f"Parsing header items: {items}")

    parsed_items: List[SortableItemType] = []
    for item in items:
        # Instantiate parsed item of type SortableItemType:
        try:
            parsed_items.append(parse(item))
        except ignore_exception:
            # Ignore allowed exception:
            logging.debug("Ignoring invalid item: %s", item)

    # Sort and return list of weighted languages:
    parsed_items.sort(reverse=True)
    logging.debug(
        f"Sorted items: {', '.join(str(p) for p in parsed_items)}"
    )  # noqa: B950

    return parsed_items
