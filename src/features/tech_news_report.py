from src.models.request_model import FlowRequest
from src.agents.flow_generation_agent import FlowGenerationAgent
from src.utils.model_adapter import ModelAdapter
from src.models.config_model import FlowGenerationConfig

class FlowGeneration:
    def __init__(self, model_adapter: ModelAdapter, flow_generation_config: FlowGenerationConfig) -> None:
        self.model_adapter = model_adapter
        self.flow_generation_config = flow_generation_config
        self.flow_generation_agent = FlowGenerationAgent(self.model_adapter,self.flow_generation_config)

    async def generate_flow(self, flow_request: FlowRequest):
        return await self.flow_generation_agent.generate_flow(flow_request)


