from collections import OrderedDict
from rest_framework.pagination import (PageNumberPagination,
                                       replace_query_param,
                                       _get_displayed_page_numbers,
                                       _get_page_links)
from rest_framework.response import Response


class DetailedPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        base_url = self.request.get_full_path()

        def page_number_to_url(pnum):
            return replace_query_param(base_url, self.page_query_param, pnum)

        current = self.page.number
        final = self.page.paginator.num_pages
        page_numbers = _get_displayed_page_numbers(current, final)
        page_links = _get_page_links(page_numbers, current, page_number_to_url)

        return Response(OrderedDict([("page_links", page_links),
                                     ("results", data)]))
