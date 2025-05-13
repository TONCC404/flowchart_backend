from pydantic import BaseModel
from typing import Optional

class BaiduConfig(BaseModel):
    api_key: str
    secret_key: str

class ModelConfig(BaseModel):
    model_version: str
    temperature: float | None = None
    response_format: str | None = None
    top_p: Optional[float] = 0.9
    max_gen_len: Optional[int] = 4096
    stream: Optional[bool] = False

class BaiduConfig(BaseModel):
    api_key: str
    secret_key: str

class FlowGenerationConfig(BaseModel):
    model: str
    modelconfig: ModelConfig

class AuditReportConfig(BaseModel):
    model: str
    modelconfig: ModelConfig

class FeaturesConfig(BaseModel):
    flow_generation: FlowGenerationConfig
    audit_report: AuditReportConfig

class MetallamaConfig(BaseModel):
    version: str
    temperature: float

class LLMModelConfig(BaseModel):
    meta_llama: MetallamaConfig
class LLMConfig(BaseModel):
    url: str
    api_key: str
    model: LLMModelConfig

class PostgresqlConfig(BaseModel):
    host: str
    port: int
    database: str
    user: str
    password: str| int
    # embedding_model: EmbeddingConfig

class GoogleConfig(BaseModel):
    client_id: str
    client_secret: str
    google_redirect_uri: str

class WeChatConfig(BaseModel):
    wechat_app_id: str
    wechat_app_secret: str
    wechat_redirect_uri: str

class PayPalConfig(BaseModel):
    paypal_client_id: str
    paypal_client_secret: str
    paypal_redirect_uri: str
    cancel_url: str

class ServiceConfig(BaseModel):
    llm: LLMConfig
    baidu: BaiduConfig
    google: GoogleConfig
    wechat: WeChatConfig
    paypal: PayPalConfig
    postgresql: PostgresqlConfig
    features: FeaturesConfig




