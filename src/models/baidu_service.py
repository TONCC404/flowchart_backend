
from src.models.config_model import ServiceConfig, ModelConfig
import requests
import json


class BaiduService:
    def __init__(self, service_config: ServiceConfig) -> None:
        self.api_key = service_config.baidu.api_key
        self.secret_key = service_config.baidu.secret_key

    def get_access_token(self):
        """
        使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
        """

        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"

        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

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
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{modelconfig.model_version}?access_token=" + self.get_access_token()


        payload = json.dumps(prompt)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text



