import time

import boto3
from botocore.exceptions import EndpointConnectionError
from oauthlib.oauth2 import InsecureTransportError, is_secure_transport
from requests_oauthlib import OAuth2

from cardmarket_api.exceptions import ApiConnectionError


class Auth(OAuth2):
    def __init__(
        self, aws_region: str, client_id: str, username=None, password=None, token=None
    ):
        """Construct a new OAuth 2 authorization object."""
        self.aws_region = aws_region
        self.client_id = client_id
        self.username = username
        self.password = password
        if not token:
            token = self.build_token()
        super(Auth, self).__init__(client_id, client=None, token=token)

    def __call__(self, r):
        """Append an OAuth 2 token to the _request."""
        if not is_secure_transport(r.url):
            raise InsecureTransportError()
        if self._client._expires_at < time.time():
            token = self.build_token()
            for k, v in token.items():
                setattr(self._client, k, v)
        r.headers.__setitem__("Authorization", self._client.id_token)
        return r

    def build_token(self):
        client = boto3.client("cognito-idp", region_name=self.aws_region)
        try:
            response = client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={"USERNAME": self.username, "PASSWORD": self.password},
            )
        except EndpointConnectionError as e:
            raise ApiConnectionError(*e.args, **e.kwargs)
        assert (
            response["ResponseMetadata"]["HTTPStatusCode"] == 200
        ), "Authentication failed"
        result = response["AuthenticationResult"]
        return {
            "token_type": result["TokenType"],
            "access_token": result["AccessToken"],
            "refresh_token": result["RefreshToken"],
            "id_token": result["IdToken"],
            "expires_in": result["ExpiresIn"],
        }
