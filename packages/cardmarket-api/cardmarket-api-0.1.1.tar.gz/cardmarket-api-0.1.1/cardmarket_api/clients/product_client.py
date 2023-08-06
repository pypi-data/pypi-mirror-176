from uuid import UUID

from .base import BaseClient


class ProductClient(BaseClient):
    """
    Products - Manage product aggregates.
    """

    def products_list(self, **kwargs):
        """
        No parameters
        """
        return self._request(
            "GET",
            "/products",
            **kwargs,
        )

    def products_detail(self, product_id: UUID, params: {} = None, **kwargs):
        """
        :product_id: An auto generated uuid used to identify the object

        :params: Custom GET parameters
        """

        params = params or {}

        return self._request("GET", f"/products/{product_id}", params=params, **kwargs)

    """
    Categories
    """

    def categories_list(
        self,
        **kwargs,
    ):
        """
        No parameters
        """
        return self._request("GET", "/categories", **kwargs)

    def categories_detail(self, category_id: UUID, **kwargs):
        """
        :category_id: An auto generated uuid used to identify the object
        """

        return self._request(
            "GET",
            f"/categories/{category_id}",
            **kwargs,
        )

    """
    Attribute Entities
    """

    def attribute_entities_list(
        self,
        **kwargs,
    ):
        """
        No parameters
        """
        return self._request(
            "GET",
            "/attributeEntities",
            **kwargs,
        )

    def attribute_entities_detail(self, attribute_entity_id: UUID, **kwargs):
        """
        :attribute_entity_id: An auto generated uuid used to identify the object
        """
        return self._request(
            "GET", f"/attributeEntities/{attribute_entity_id}", **kwargs
        )

    def attribute_entities_detail_instances_list(
        self,
        attribute_entity_id: UUID,
        **kwargs,
    ):
        """
        :attribute_entity_id: An auto generated uuid used to identify the object
        """
        return self._request(
            "GET",
            f"/attributeEntities/{attribute_entity_id}/instances",
            **kwargs,
        )

    def attribute_entities_detail_instances_detail(
        self,
        attribute_entity_id: UUID,
        attribute_entity_instance_id: UUID,
        **kwargs,
    ):
        """
        :attribute_entity_id: An auto generated uuid used to identify the object
        :attribute_entity_instance_id: An auto generated uuid used to identify the object
        """
        return self._request(
            "GET",
            f"/attributeEntities/{attribute_entity_id}/instances/{attribute_entity_instance_id}",
            **kwargs,
        )

    """
    Attributes
    """

    def product_attributes_list(
        self,
        **kwargs,
    ):
        """
        No parameters
        """
        return self._request("GET", "/productAttributes", **kwargs)

    def product_attributes_detail(
        self,
        product_attribute_id: UUID,
        **kwargs,
    ):
        """
        :product_attribute_id: An auto generated uuid used to identify the object
        """
        return self._request(
            "GET", f"/productAttributes/{product_attribute_id}", **kwargs
        )

    def article_attributes_list(
        self,
        **kwargs,
    ):
        """
        No parameters
        """
        return self._request("GET", "/articleAttributes", **kwargs)

    def article_attributes_detail(
        self,
        article_attribute_id: UUID,
        **kwargs,
    ):
        """
        :article_attribute_id: An auto generated uuid used to identify the object
        """
        return self._request(
            "GET", f"/articleAttributes/{article_attribute_id}", **kwargs
        )
