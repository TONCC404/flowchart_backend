import json

from src.models.config_model import ServiceConfig, ModelConfig
import requests


class LLMService:
    def __init__(self, service_config: ServiceConfig) -> None:
        self.service_config = service_config
        self.api_key = service_config.llm.api_key


    async def async_chat_completion_calls(self, prompt, modelconfig: ModelConfig = None):
        """prompt format is:
        {
            "messages": [
                {
                    "role": "user",
                    "content": "你好"
                }
            ]
        }"""
        url = self.service_config.llm.url
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        data = {
            "model": modelconfig.model_version,
            "messages": prompt["messages"]
        }

        response = requests.post(url, headers=headers, json=data)
        response = json.loads(response.text)
        return response["choices"][0]["message"]["content"]



