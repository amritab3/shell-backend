from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 12
    page_query_param = "page"

    # def get_paginated_response(self, data):
    #     paginated_response = super(CustomPageNumberPagination, self).get_paginated_response(data)
    #     paginated_response.data['pages'] = self.page.paginator.num_pages
    #     return paginated_response

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.page_size,
                "current_page_number": self.page.number,
                "results": data,
            }
        )
