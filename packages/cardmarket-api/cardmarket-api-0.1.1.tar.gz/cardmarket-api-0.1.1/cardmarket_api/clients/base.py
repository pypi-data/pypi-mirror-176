import typing

from requests import HTTPError, request

from ..exceptions import ApiException

if typing.TYPE_CHECKING:
    from ..auth import Auth


class BaseClient:
    def __init__(
        self,
        base_endpoint: str,
        auth: "Auth",
    ):
        self.base_endpoint = base_endpoint
        self._auth = auth

    def _request(
        self,
        method: str,
        url: str,
        json: {} = None,
        **kwargs,
    ):
        complete_url = f"{self.base_endpoint}{url}"
        response = request(
            method=method, url=complete_url, auth=self._auth, json=json, **kwargs
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise ApiException(response=response)
        return response.json() if response.content else {}
