from rest_framework.pagination import LimitOffsetPagination


class AccountPagination(LimitOffsetPagination):
    default_limit = 15
    max_limit = 15
    limit_query_param = "limit"
    offset_query_param = "offset"


class HashtagPagination(LimitOffsetPagination):
    default_limit = 69
    max_limit = 69
    limit_query_param = "limit"
    offset_query_param = "offset"


class NotificationPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 50
    limit_query_param = "limit"
    offset_query_param = "offset"


class PhotoPagination(LimitOffsetPagination):
    default_limit = 18
    max_limit = 18
    limit_query_param = "limit"
    offset_query_param = "offset"


class ShopPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 50
    limit_query_param = "limit"
    offset_query_param = "offset"
