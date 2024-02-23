from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination size"""
    page_size = 12
    page_size_query_param = 'page'
