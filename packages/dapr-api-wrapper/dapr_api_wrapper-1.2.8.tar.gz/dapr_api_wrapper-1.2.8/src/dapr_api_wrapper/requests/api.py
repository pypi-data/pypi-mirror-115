from .request import DaprRequest


def request(http_method=None, **kwargs) -> DaprRequest:
    kwargs.pop("http_method", None)
    return DaprRequest(http_method=http_method, **kwargs)


def head(**kwargs):
    return request(http_method="HEAD", **kwargs)


def options(**kwargs):
    return request(http_method="OPTIONS", **kwargs)


def get(**kwargs):
    return request(http_method="GET", **kwargs)


def post(**kwargs) -> DaprRequest:
    return request(http_method="POST", **kwargs)


def patch(**kwargs):
    return request(http_method="PATCH", **kwargs)


def put(**kwargs):
    return request(http_method="PUT", **kwargs)


def delete(**kwargs):
    return request(http_method="DELETE", **kwargs)
