from rest_framework.pagination import LimitOffsetPagination


class AccountPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 150
    limit_query_param = "limit"
    offset_query_param = "offset"


class HashtagPagination(LimitOffsetPagination):
    default_limit = 18
    max_limit = 100
    limit_query_param = "limit"
    offset_query_param = "offset"


class NotificationPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50
    limit_query_param = "limit"
    offset_query_param = "offset"


class PhotoPagination(LimitOffsetPagination):
    default_limit = 18
    max_limit = 250
    limit_query_param = "limit"
    offset_query_param = "offset"


class ShopPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 250
    limit_query_param = "limit"
    offset_query_param = "offset"
