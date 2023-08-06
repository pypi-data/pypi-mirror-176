from requests import ConnectionError, HTTPError


class ApiException(HTTPError):
    def __str__(self):
        return f"{self.response.status_code}: {self.response.content.decode()}"


class ApiConnectionError(ConnectionError):
    def __init__(self, *args, **kwargs):
        self.endpoint_url = kwargs.pop("endpoint_url", None)
        self.error = kwargs.pop("error", None)
        super(ApiConnectionError, self).__init__(*args, **kwargs)
