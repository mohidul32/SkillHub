from rest_framework.pagination import PageNumberPagination

class CoursePagination(PageNumberPagination):
    page_size = 10  # default page size
    page_size_query_param = 'page_size'  # ?page_size=20
    max_page_size = 100
