import uuid
from uuid import UUID

from .base import BaseClient


class MarketplaceClient(BaseClient):
    """
    Articles - Endpoints used to manage your inventory on Cardmarket
    """

    def articles_list(
        self,
        account_id: UUID = None,
        product_id: UUID = None,
        binder_id: UUID = None,
        in_shopping_cart: bool = None,
        params: {} = None,
        **kwargs,
    ):
        """
        :account_id: Only available to Marketplace and Super admins.
        :product_id: An auto generated uuid used to identify the object.
        :binder_id: An auto generated uuid used to identify the object.
        :in_shopping_cart:

        :params: Custom GET parameters
        """
        params = params or {}

        if account_id:
            params.setdefault("accountId", account_id)
        if product_id:
            params.setdefault("productId", product_id)
        if binder_id:
            params.setdefault("binderId", binder_id)
        if in_shopping_cart is not None:
            params.setdefault("inShoppingCart", in_shopping_cart)

        return self._request(
            "GET",
            "/articles",
            params=params,
            **kwargs,
        )

    def articles_create(
        self,
        product_id: UUID,
        binder_id: UUID = None,
        comment: str = None,
        seller_note: str = None,
        article_attribute_instances_ids: {} = None,
        price: {} = None,
        quantity: int = None,
        json: dict = None,
        **kwargs,
    ):

        """
        :product_id: An auto generated uuid used to identify the object.
        :binder_id: An auto generated uuid used to identify the object.
        :comment:
        :seller_note:
        :article_attribute_instances_ids: Example: {"additionalProp1": true}
        :price: Example: {"currencyId": "EUR", "value": 11.11}
        :quantity:

        :json: Custom POST json
        """
        json = json or {}
        article_attribute_instances_ids = article_attribute_instances_ids or {}

        if product_id is not None:
            json.setdefault("productId", product_id)
        if binder_id is not None:
            json.setdefault("binderId", binder_id)
        if comment is not None:
            json.setdefault("comment", comment)
        if seller_note is not None:
            json.setdefault("sellerNote", seller_note)
        if article_attribute_instances_ids is not None:
            json.setdefault(
                "articleAttributeInstancesIds", article_attribute_instances_ids
            )
        if price is not None:
            json.setdefault("price", price)
        if quantity is not None:
            json.setdefault("quantity", quantity)

        return self._request("POST", "/articles/", json=[json], **kwargs)

    """
    Binders - Endpoints for organising your inventory
    """

    def binders_list(
        self,
        binders_ids: [UUID] = None,
        params: {} = None,
        **kwargs,
    ):
        """
        :binders_ids: List of an auto generated uuids used to identify the objects.
        """
        params = params or {}

        if binders_ids:
            params.setdefault("binderIds", binders_ids)

        return self._request(
            "GET",
            "/binders",
            params=params,
            **kwargs,
        )

    def binders_create(
        self,
        name: str = None,
        description: str = None,
        is_on_sale: bool = None,
        is_default: bool = None,
        binder_id: UUID = str(uuid.uuid4()),
        json: dict = None,
        **kwargs,
    ):

        """
        :name:
        :description:
        :is_on_sale:
        :is_default:

        :json: Custom POST json
        """
        json = json or {}

        if name:
            json.setdefault("name", name)
        if description:
            json.setdefault("description", description)
        if is_on_sale is not None:
            json.setdefault("isOnSale", is_on_sale)
        if is_default is not None:
            json.setdefault("isDefault", is_default)
        if binder_id:
            json.setdefault("id", binder_id)

        return self._request("POST", "/binders/", json=json, **kwargs)

    def binders_update(
        self,
        binder_id: UUID,
        name: str = None,
        description: str = None,
        is_on_sale: bool = None,
        is_default: bool = None,
        json: dict = None,
        **kwargs,
    ):
        """
        :binder_id: An auto generated uuid used to identify the object

        :name:
        :description:
        :is_on_sale:
        :is_default:

        :json: Custom POST json
        """
        json = json or {}

        if name:
            json.setdefault("name", name)
        if description:
            json.setdefault("description", description)
        if is_on_sale is not None:
            json.setdefault("isOnSale", is_on_sale)
        if is_default is not None:
            json.setdefault("isDefault", is_default)
        return self._request("PATCH", f"/binders/{binder_id}/", json=json, **kwargs)

    def binders_delete(
        self,
        binder_id: UUID,
        **kwargs,
    ):
        """
        :binder_id: An auto generated uuid used to identify the object
        """
        return self._request("DELETE", f"/binders/{binder_id}", **kwargs)
