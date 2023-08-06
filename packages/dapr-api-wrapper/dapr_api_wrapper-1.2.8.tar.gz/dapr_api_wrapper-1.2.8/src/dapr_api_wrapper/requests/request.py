from json import dumps, loads
from typing import Optional, Union
from urllib.parse import urlparse
from warnings import warn

from dapr.clients import DaprClient

from .exceptions import ImplementationError


class DaprRequest:
    """
    from dapr_api_wrapper import requests as dapr_requests
    from datetime import datetime

    test_body = {
        "id": "12345",
        "api_key": "1234567",
        "updated_at": str(datetime.now()),
        "num": 1234567,
        "is_auth": True,
    }

    resp = dapr_requests.post(
        app_id="myawesome-svc",
        url_path="http://myawesome-svc-svc/test",
        data=test_body,
        content_type="application/json",
        headers={"key1": "value1"},
        http_query_params={"querykey1": "queryvalue1"},
    )
    resp_json = resp.json()

    resp_text = resp.text

    resp_bytes = resp.bytes()
    """

    def __init__(
        self,
        app_id: str,
        url_path: Optional[str] = None,
        http_method: Optional[str] = None,
        http_query_params: Optional[dict] = None,
        headers: Optional[dict] = None,
        data: Union[dict,  list,  str,  bytes] = None,
        content_type: str = "application/json",
        metadata: Optional[dict] = None,
        is_grpc: Optional[bool] = False,
        grpc_method: Optional[str] = None,
    ):
        """
        Args:
            app_id (str): the callee app id
            url_path (str): full kubernetes svc url
            http_method (str): http_method assigned at url_path
            http_query_params (dict): key-value pairs to represent query string
            headers (dict): key-value pairs to represent headers
            meta_data (dict): any additional key-value pairs
            grpc_method (str): name of the method hosted on grpc server
            data (dict or list or str or bytes): data to send
            content_type (str): content_type of data to receive
            is_grpc (bool): set to  True if grpc method is specified
        """
        self.invoke_kwargs = {
            "app_id": app_id,
            "content_type": content_type,
        }

        self.data = data

        if is_grpc:
            if not grpc_method:
                raise ImplementationError(
                    "grpc_method is required since you have set is_grpc=True"
                )
            if http_method:
                warn("grpc is enabled and so http method will have no effect")

            self.invoke_kwargs["method_name"] = grpc_method

        else:
            if not http_method:
                raise ImplementationError(
                    "please specify one of http_method or grpc_method"
                )
            if not url_path:
                raise ImplementationError(
                    "url_path is required in in case of http_method"
                )

            self.invoke_kwargs["method_name"] = self.__get_method_name(url_path)
            self.invoke_kwargs["http_verb"] = http_method

        self.invoke_kwargs["data"] = self.__handle_data(data=data)

        self.__handle_additional_dict(
            dapr_invoke_param="http_querystring", _dict=http_query_params
        )
        self.__handle_additional_dict(dapr_invoke_param="metadata", _dict=headers)
        self.__handle_additional_dict(dapr_invoke_param="metadata", _dict=metadata)

        self.__execute()

    def __handle_additional_dict(self, dapr_invoke_param: str, _dict=None):
        if _dict:
            if isinstance(_dict, dict):
                if dapr_invoke_param == "metadata":
                    if "metadata" in self.invoke_kwargs:
                        self.invoke_kwargs["metadata"] += tuple(_dict.items())
                    else:
                        self.invoke_kwargs["metadata"] = tuple(_dict.items())
                else:
                    self.invoke_kwargs[dapr_invoke_param] = tuple(_dict.items())

            else:
                raise TypeError(f"{_dict} is not an of instance dict")

    def __handle_data(self, data):
        if data is not None:
            if isinstance(data, (dict, list)):
                data = dumps(data).encode("utf-8")

            elif isinstance(data, str):
                data = data.encode("utf-8")

            elif isinstance(data, bytes):
                pass

            else:
                raise TypeError(
                    f"{data} is not an instance of dict or list or str, or bytes"
                )

        else:
            data = b""

        return data

    def __get_method_name(self, url: str):
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return result.path.lstrip("/")
        return url.lstrip("/")

    def __execute(self):
        with DaprClient() as dapr_client:
            self.resp = dapr_client.invoke_method(**self.invoke_kwargs)

    @property
    def text(self):
        return self.resp.text()

    def bytes(self):
        return self.resp.data

    def json(self):
        return loads(self.bytes())
