from uuid import UUID

from .base import BaseClient


class UserClient(BaseClient):
    """
    Account - Everything related to both account types
    """

    def accounts_list(
        self,
        username: str = None,
        account_type: str = None,
        country: str = None,
        is_powerseller: bool = None,
        params: {} = None,
        **kwargs,
    ):
        """
        :username: Available to everyone
        :account_type: Available to everyone (Private, Business)
        :country: ISO-3166 ALPHA-2 (D == DE)
        :is_powerseller: Available to everyone

        :params: Custom GET parameters
        """

        params = params or {}

        assert account_type in (None, "Private", "Business")

        if username is not None:
            params.setdefault("username", username)
        if account_type is not None:
            params.setdefault("accountType", account_type)
        if country is not None:
            params.setdefault("country", country)
        if is_powerseller is not None:
            params.setdefault("isPowerseller", is_powerseller)

        return self._request("GET", "accounts", params=params, **kwargs)

    def accounts_detail(
        self,
        account_id: UUID,
        min_version: int = None,
        params: {} = None,
        **kwargs,
    ):
        """

        :account_id: An auto generated uuid used to identify the object

        :min_version:

        :params: Custom GET parameters
        """
        params = params or {}

        if min_version is not None:
            params.setdefault("min_version", min_version)

        return self._request("GET", f"accounts/{account_id}", params=params, **kwargs)

    def accounts_add_photo_id(
        self,
        account_id: UUID,
        file_name: str = None,
        content_url: str = None,
        json: {} = None,
        **kwargs,
    ):
        """
        Uploads photo identification to be reviewed.

        :account_id: An auto generated uuid used to identify the object

        :file_name:
        :content_url: Example: https://www.example.com/image

        :json: Custom POST json
        """
        json = json or {}

        if file_name:
            json.setdefault("fileName", file_name)
        if content_url:
            json.setdefault("contentUrl", content_url)

        return self._request(
            "POST", f"accounts/{account_id}/addPhotoId", json=json, **kwargs
        )

    def accounts_add_business_registration(
        self,
        account_id: UUID,
        file_name: str = None,
        content_url: str = None,
        json: {} = None,
        **kwargs,
    ):
        """
        Uploads a business registration to be reviewed

        :account_id: An auto generated uuid used to identify the object

        :file_name:
        :content_url: Example: https://www.example.com/image

        :json: Custom POST json
        """
        json = json or {}

        if file_name:
            json.setdefault("fileName", file_name)
        if content_url:
            json.setdefault("contentUrl", content_url)

        return self._request(
            "POST",
            f"accounts/{account_id}/addBusinessRegistration/",
            json=json,
            **kwargs,
        )

    def accounts_update_username(
        self, account_id: UUID, username: str = None, json: {} = None, **kwargs
    ):
        """
        :account_id: An auto generated uuid used to identify the object

        :username: New username to update

        :json: Custom POST json
        """
        json = json or {}

        if username:
            json.setdefault("username", username)

        return self._request(
            "POST", f"accounts/{account_id}/updateUsername/", json=json, **kwargs
        )

    """
    Notifications
    """

    def notifications_list(
        self,
        account_id: UUID,
        notification_min_date: str = None,
        params: {} = None,
        **kwargs,
    ):
        """
        :account_id: An auto generated uuid used to identify the object

        :notification_min_date: Example: "1970-01-01 00:00:00"

        :params: Custom GET parameters
        """
        params = params or {}

        params["accountId"] = account_id
        if notification_min_date:
            params.setdefault("notificationMinDate", notification_min_date)

        return self._request("GET", "/notifications", params=params, **kwargs)
