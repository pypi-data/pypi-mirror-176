from typing import Any, Dict, List
from rest_framework import pagination


def create_page(
    count: int, results: List[Any], next: str = None, previous: str = None
) -> Dict[str, Any]:
    return {
        "count": count,
        "next": next,
        "previous": previous,
        "results": results,
    }


class PageNumberPagination(pagination.PageNumberPagination):
    """
    Overriden to allow client to control the page size.
    """

    page_size = 10
    page_size_query_param = "size"
