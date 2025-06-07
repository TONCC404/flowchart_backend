from pydantic import BaseModel
from typing import List, Dict, Any, Literal

class FlowRequest(BaseModel):
    prompt: str        #user prompt from UI

class AuditReportRequest(BaseModel):
    prompt: str        #user prompt from UI

class LoginRequest(BaseModel):
    action: Literal['email_verification', 'password_verification']
    username: str
    password: str | None = None
    verification_code: str | None = None

class RegisterRequest(BaseModel):
    username: str
    password: str
    organization: str | None = None
    industry: str | None = None
    team: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar_url: str| None = None
    collaborators: List[str] | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class Node(BaseModel):
    id: str
    position: Dict[str, Any]
    data: Dict[str, Any]
    isVirtual: bool
    size:Dict[str, Any]
    connectionPoints: List[Any]

class Edge(BaseModel):
    id: str
    arrowHead: bool
    isVirtual: bool
    source: Dict[str, Any]
    target: Dict[str, Any]
    sourceConnectionPoint: Dict[str, Any]
    targetConnectionPoint: Dict[str, Any]

class Flow(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class FlowChart(BaseModel):
    flow_id: str
    name: str
    data: Flow

class SaveFlowRequest(BaseModel):
    username: str|None = None
    user_id: str
    flowchart: FlowChart

class DeleteFlowRequest(BaseModel):
    username: str
    user_id: str
    flow_id: str

class CardPaymentRequest(BaseModel):
    amount: int  # in cents
    currency: str
    plan_name: str
    email: str

class PayPalOrderRequest(BaseModel):
    amount: float
    planName: str | None

class QueryFlowRequest(BaseModel):
    user_id: str
