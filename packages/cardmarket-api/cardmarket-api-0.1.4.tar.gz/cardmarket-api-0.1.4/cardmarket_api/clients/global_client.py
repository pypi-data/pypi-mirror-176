from .base import BaseClient


class GlobalClient(BaseClient):
    def retrieve_token_post(
        self, username: str = None, password: str = None, json: dict = None, **kwargs
    ):
        """
        Endpoint that allows the user to retrieve an access token for their account.
        """

        json = json or {}
        if username is not None:
            json.setdefault("username", username)
        if password is not None:
            json.setdefault("password", password)

        return self._request(
            "POST",
            "RetrieveToken",
            json=json,
            **kwargs,
        )
