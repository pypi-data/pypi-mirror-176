from . import clients
from .auth import Auth

DOMAIN_MAPPING = {
    "global": "https://global{stage}.cardmarket.com/v3",
    "user": "https://user{stage}.cardmarket.com/v3",
    "product": "https://product{stage}.cardmarket.com/v3",
    "marketplace": "https://marketplace{stage}.cardmarket.com/v3",
}


class CardMarketApi:
    def __init__(
        self,
        auth: Auth = None,
        username: str = None,
        password: str = None,
        client_id: str = "15kh0e0f04o1iaq5ie8jf78fuh",
        aws_region: str = "eu-central-1",
        sandbox=False,
    ):
        """
        :sandbox: Sandbox mode vs Production
        """
        self.sandbox = sandbox
        if not auth:
            self.auth = Auth(aws_region, client_id, username, password)
        else:
            self.auth = auth

        def get_base_endpoint(domain):
            return DOMAIN_MAPPING[domain].format(stage=".sandbox" if sandbox else "")

        self.global_client = clients.GlobalClient(
            base_endpoint=get_base_endpoint("global"), auth=self.auth
        )
        self.user = clients.UserClient(
            base_endpoint=get_base_endpoint("user"),
            auth=self.auth,
        )
        self.product = clients.ProductClient(
            base_endpoint=get_base_endpoint("product"),
            auth=self.auth,
        )
        self.marketplace = clients.MarketplaceClient(
            base_endpoint=get_base_endpoint("marketplace"),
            auth=self.auth,
        )
        super(CardMarketApi, self).__init__()
