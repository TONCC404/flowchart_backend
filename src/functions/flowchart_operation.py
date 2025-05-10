from src.utils.model_adapter import ModelAdapter
from src.utils.postgres_service import PostgresqlService
from src.models.request_model import SaveFlowRequest, DeleteFlowRequest, QueryFlowRequest


class FlowChartOperation:
    def __init__(self, model_adapter: ModelAdapter, postgresql_service: PostgresqlService) -> None:
        self.model_adapter = model_adapter
        self.postgresql_service = postgresql_service

    async def save_flowchart(self, request: SaveFlowRequest):

        flow_id = request.flowchart.flow_id
        name = request.flowchart.name
        data = request.flowchart.data
        user_id = request.user_id
        result = await self.postgresql_service.save_flow(flow_id, name, data, user_id)
        return result


    async def delete_flowchart(self, request: DeleteFlowRequest):
        flow_id = request.flow_id
        result = await self.postgresql_service.delete_flow(flow_id)
        return result


    async def query_flowlist(self, request: QueryFlowRequest):
        user_id = request.user_id
        result = await self.postgresql_service.query_flowlist(user_id)
        return result