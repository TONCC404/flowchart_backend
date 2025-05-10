import logging
from src.utils.config_loader import SERVICE_CONFIG
from src.models.baidu_service import BaiduService
from src.models.llm_service import LLMService
from src.models.config_model import ModelConfig
from typing import Any

logger = logging.getLogger(__name__)

class ModelAdapter:
    def __init__(self, service_config: SERVICE_CONFIG) -> None:
        self.baidu_service = BaiduService(service_config=service_config)
        self.llm_service = LLMService(service_config=service_config)
    async def model_async_call(self, model: str, prompt: Any, model_config: ModelConfig = None) -> Any:
        if model in ("baidu"):
            result = await self.baidu_service.async_chat_completion_calls(prompt, model_config)
            if(model_config.stream == True):
                return result
            else:
                return result
        if model in ("llm"):
            result = await self.llm_service.async_chat_completion_calls(prompt, model_config)
            if(model_config.stream == True):
                return result
            else:
                return result

