from src.models.request_model import AuditReportRequest
import logging
from src.utils.model_adapter import ModelAdapter
from src.models.config_model import AuditReportConfig
from src.utils.prompt_loader import load_prompt
from pathlib import Path

logger = logging.getLogger(__name__)
class AuditAgent:
    def __init__(self, model_adapter: ModelAdapter, audit_report_config: AuditReportConfig) -> None:
        self.model_adapter = model_adapter
        self.audit_report_config = audit_report_config

    async def generate_audit_report(self, audit_report_request: AuditReportRequest):

        user_prompt = audit_report_request["prompt"]

        sys_prompt = load_prompt(Path() / "Audit" / "audit_report_generate_sys_prompt")
        ChatPrompt = {
            "messages":[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ]}
        try:
            logger.info(f'Agents start generating audit report')
            logger.info(f'AuditReport Request is:{audit_report_request}')
            result = await self.model_adapter.model_async_call(model = self.audit_report_config.model, prompt = ChatPrompt, model_config = self.audit_report_config.modelconfig)
            logger.info(f'result is:{result}')

        except Exception as error:
            logger.error(f"ChatAgent generate questions error: {error}", exc_info=True)
            result = {
                "error_code" : 6,
                "status" : "filter with users error",
                "error_message" : repr(error)
            }
        return result

    async def analyze_financial_report(self, audit_report_request: AuditReportRequest, file_content):

        user_prompt = audit_report_request["prompt"]

        sys_prompt = load_prompt(Path() / "Audit" / "analyze_financial_report_sys_prompt")
        ChatPrompt = {
            "messages":[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ]}
        try:
            logger.info(f'Agents start analyzing financial report')
            logger.info(f'Financial Request is:{audit_report_request}')
            result = await self.model_adapter.model_async_call(model = self.audit_report_config.model, prompt = ChatPrompt, model_config = self.audit_report_config.modelconfig)
            logger.info(f'result is:{result}')

        except Exception as error:
            logger.error(f"Audit Agent analyze the financial report error: {error}", exc_info=True)
            result = {
                "error_code" : 6,
                "status" : "filter with users error",
                "error_message" : repr(error)
            }
        return result