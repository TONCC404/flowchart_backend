import httpx
from typing import Optional
from src.utils.config_loader import SERVICE_CONFIG

class PayPalClient:
    def __init__(self, sandbox: bool = True):
        self.service_config = SERVICE_CONFIG.paypal
        self.client_id = self.service_config.paypal_client_id
        self.client_secret = self.service_config.paypal_client_secret
        self.base_url = "https://api-m.sandbox.paypal.com" if sandbox else "https://api-m.paypal.com"
        self.access_token = None
        self.return_url = self.service_config.paypal_redirect_uri
        self.cancel_url = self.service_config.cancel_url

    async def get_access_token(self) -> str:
        async with httpx.AsyncClient() as client:
            auth = (self.client_id, self.client_secret)
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {"grant_type": "client_credentials"}

            resp = await client.post(f"{self.base_url}/v1/oauth2/token", data=data, headers=headers, auth=auth)
            resp.raise_for_status()
            self.access_token = resp.json()["access_token"]
            return self.access_token

    async def create_order(self, amount: float):
        if not self.access_token:
            await self.get_access_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": f"{amount:.2f}"
                    }
                }
            ],
            "application_context": {
                "return_url": self.return_url,
                "cancel_url": self.cancel_url
            }
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/v2/checkout/orders", headers=headers, json=order_data)
            resp.raise_for_status()
            data = resp.json()
            for link in data.get("links", []):
                if link.get("rel") == "approve":
                    res_url = link.get("href")
                    return {"approvalUrl": res_url}
            return None
