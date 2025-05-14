from src.utils.model_adapter import ModelAdapter
from src.utils.postgres_service import PostgresqlService
from src.models.request_model import LoginRequest, RegisterRequest
from src.utils.token_verification import create_access_token
from fastapi import HTTPException
from src.utils.config_loader import SERVICE_CONFIG,oauth
from src.utils.log_config import log_config
from src.payment.paypal_service import PayPalClient
logger = log_config()

class BillAccountOperation:
    def __init__(self, model_adapter: ModelAdapter, postgresql_service: PostgresqlService) -> None:
        self.model_adapter = model_adapter
        self.postgresql_service = postgresql_service
        self.oauth = oauth
        self.service_config = SERVICE_CONFIG
        self.paypal_client = PayPalClient()

    async def paypal_account_operation(self, amount) -> str:
        return await self.paypal_client.create_order(amount)