=====
Usage
=====

To use Cardmakret API v3+ in a project::

        from cardmarket_api import CardMarketApi

        api = CardMarketApi(
            username="username",
            password="password",
            sandbox=True,
        )

        # Binders
        ## Create binder
        api.marketplace.binders_create(
            name="Monty Python",
        )
        binders = api.marketplace.binders_list()
        binder_id = binders[-1]["id"]

        # Product
        ## List products
        products = api.product.products_list()
        product_id = products[-1]["id"]

        ## Article attributes
        article_attributes_list = api.product.article_attributes_list()
        (foil, condition, language, *_) = article_attributes_list

        (is_not_foil, is_foil) = api.product.attribute_entities_detail_instances_list(foil["attributeEntityId"])
        (nm, mt, ex) = api.product.attribute_entities_detail_instances_list(condition["attributeEntityId"])
        (de, en) = api.product.attribute_entities_detail_instances_list(language["attributeEntityId"])

        # Marketplace
        ## Create article
        api.marketplace.articles_create(
            product_id=product_id,
            binder_id=binder_id,
            price={
                "currencyId": "EUR",
                "value": 11.11
            },
            quantity=1,
            article_attribute_instances_ids={
                is_foil["id"]: True,
                nm["id"]: True,
                en["id"]: True,
            },
        )

        ## List articles in marketplace
        articles = api.marketplace.articles_list()
