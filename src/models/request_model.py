from pydantic import BaseModel
from typing import List, Dict, Any

class FlowRequest(BaseModel):
    prompt: str        #user prompt from UI

class AuditReportRequest(BaseModel):
    prompt: str        #user prompt from UI

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str | None = None
    phone: str | None = None
    avatar_url: str| None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class Node(BaseModel):
    node_id: str
    position: Dict[str, Any]
    data: Dict[str, Any]

class Edge(BaseModel):
    edge_id: str
    source_node: Dict[str, Any]
    target_node: Dict[str, Any]

class Flow(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class FlowChart(BaseModel):
    flow_id: str
    name: str
    data: Flow

class SaveFlowRequest(BaseModel):
    username: str
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
