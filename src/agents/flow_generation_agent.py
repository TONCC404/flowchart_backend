from src.models.request_model import FlowRequest
import logging
from src.utils.model_adapter import ModelAdapter
from src.models.config_model import FlowGenerationConfig
from src.utils.prompt_loader import load_prompt
from pathlib import Path

logger = logging.getLogger(__name__)
class FlowGenerationAgent:
    def __init__(self, model_adapter: ModelAdapter, flow_generation_config: FlowGenerationConfig) -> None:
        self.model_adapter = model_adapter
        self.flow_generation_config = flow_generation_config

    async def generate_flow(self, flow_request: FlowRequest):

        user_prompt = flow_request.prompt

        sys_prompt = load_prompt(Path() / "Flowchart" /"flowchat_sys_prompt_1")
        ChatPrompt = {
            "messages":[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ]}
        try:
            logger.info(f'Agents start generating workflow')
            logger.info(f'FlowGeneration Request is:{flow_request}')
            result = await self.model_adapter.model_async_call(model = self.flow_generation_config.model, prompt = ChatPrompt, model_config = self.flow_generation_config.modelconfig)
            logger.info(f'result is:{result}')

        except Exception as error:
            logger.error(f"ChatAgent generate questions error: {error}", exc_info=True)
            result = {
                "error_code" : 6,
                "status" : "filter with users error",
                "error_message" : repr(error)
            }
        return result