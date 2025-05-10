from src.models.request_model import AuditReportRequest
from src.agents.audit_agent import AuditAgent
from src.utils.model_adapter import ModelAdapter
from src.models.config_model import AuditReportConfig

class AuditReportGeneration:
    def __init__(self, model_adapter: ModelAdapter, audit_report_config: AuditReportConfig) -> None:
        self.model_adapter = model_adapter
        self.audit_report_config = audit_report_config
        self.audit_agent = AuditAgent(self.model_adapter,self.audit_report_config)

    async def generate_audit_report(self, audit_request: AuditReportRequest, UPLOAD_FOLDER):
        with open(UPLOAD_FOLDER,'r') as f:
            content = f.read()
            analyze_report_result = await self.audit_agent.analyze_financial_report(audit_request, content)
            return analyze_report_result


