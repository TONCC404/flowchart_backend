from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.features.generate_flow import FlowGeneration

from src.functions.flowchart_operation import FlowChartOperation
from src.utils.config_loader import SERVICE_CONFIG
from src.utils.model_adapter import ModelAdapter
import json
from pathlib import Path
from src.models.request_model import FlowRequest, LoginRequest, RegisterRequest, SaveFlowRequest, DeleteFlowRequest, QueryFlowRequest
from src.utils.postgres_service import PostgresqlService
from starlette.middleware.sessions import SessionMiddleware
import secrets

model_adapter = ModelAdapter(service_config=SERVICE_CONFIG)
postgresql_service = PostgresqlService(service_config=SERVICE_CONFIG)
app = FastAPI()

# Configure CORS
origins = ["https://yiyan.baidu.com",
           "http://localhost:3000",
           "http://localhost:8000",
           "http://127.0.0.1:3000",
           "http://127.0.0.1:8000",
            "https://google.com"
           ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
secret_key = secrets.token_hex(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key, same_site="lax",https_only=False)
from src.functions.user_info_operation import UserInfoOperation

def make_json_response(data, status_code=200):
    return JSONResponse(content=data, status_code=status_code)

@app.post("/generate_flow_picture")
async def generate_sentences(flow_request: FlowRequest):
    """
    Generate a flow chart
    """
    try:
        flow_generation = FlowGeneration(
            model_adapter=model_adapter,
            flow_generation_config=SERVICE_CONFIG.features.flow_generation
        )
        result = await flow_generation.generate_flow(flow_request)

        if result:
            res = {"content": result}
            print(result)
        else:
            res = {}
            print("No Mermaid chart definition found")

        return {"results": res, "prompt": flow_request.get("prompt", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/user_login")
async def user_login(login_request: LoginRequest):
    user_info_operation = UserInfoOperation(model_adapter=model_adapter, postgresql_service=postgresql_service)
    result = await user_info_operation.login_service(login_request)
    return result

@app.get('/google_login')
async def login_via_google(request: Request):
    user_info_operation = UserInfoOperation(model_adapter=model_adapter, postgresql_service=postgresql_service)
    return await user_info_operation.google_redirect_callback(request)

@app.get('/google_authorize')
async def auth_callback(request: Request):
    try:
        print(request)
        user_info_operation = UserInfoOperation(model_adapter=model_adapter, postgresql_service=postgresql_service)
        result = await user_info_operation.google_oauth_callback(request)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @app.get("/wechat_login")
# async def wechat_login():
#     """
#     Get WeChat login QR code URL.
#     """
#     state = uuid.uuid4().hex
#     wechat_qr_url = (
#         f"https://open.weixin.qq.com/connect/qrconnect"
#         f"?appid={WECHAT_APP_ID}&redirect_uri={WECHAT_REDIRECT_URI}"
#         f"&response_type=code&scope=snsapi_login&state={state}"
#     )
#     return {"qr_url": wechat_qr_url, "state": state}
#
#
# @app.get("/wechat-login-callback")
# async def wechat_login_callback(code: str = Query(...), state: str = Query(...)):
#     """
#     Handle WeChat login callback.
#     """
#     # 获取 access_token 和 openid
#     token_url = (
#         f"https://api.weixin.qq.com/sns/oauth2/access_token"
#         f"?appid={WECHAT_APP_ID}&secret={WECHAT_APP_SECRET}&code={code}&grant_type=authorization_code"
#     )
#     token_response = requests.get(token_url).json()
#
#     if "errcode" in token_response:
#         raise HTTPException(status_code=400, detail="Failed to authenticate with WeChat")
#
#     access_token = token_response["access_token"]
#     openid = token_response["openid"]
#
#     user_info_url = (
#         f"https://api.weixin.qq.com/sns/userinfo"
#         f"?access_token={access_token}&openid={openid}"
#     )
#     user_info = requests.get(user_info_url).json()
#
#     if "errcode" in user_info:
#         raise HTTPException(status_code=400, detail="Failed to fetch user info")
#
#     # 检查 openid 是否已注册
#     for username, user in USER_DB.items():
#         if user.get("openid") == openid:
#             jwt_token = create_access_token(data={"sub": username})
#             return {
#                 "access_token": jwt_token,
#                 "token_type": "bearer",
#                 "avatar": user["avatar"],
#             }
#
#     return JSONResponse(
#         status_code=200,
#         content=jsonable_encoder(
#             {
#                 "message": "WeChat login successful, please bind or register an account.",
#                 "wechat_user_info": user_info,
#             }
#         ),
#     )


@app.post("/register")
async def register_user(register_request: RegisterRequest):
    user_info_operation = UserInfoOperation(model_adapter=model_adapter, postgresql_service=postgresql_service)
    result = await user_info_operation.register(register_request)
    return result

@app.post("/save_flow")
async def save_flow(save_flow_request: SaveFlowRequest):
    flowchart_operation = FlowChartOperation(model_adapter=model_adapter, postgresql_service=postgresql_service)
    result = await flowchart_operation.save_flowchart(save_flow_request)
    return result


@app.post("/delete_flow")
async def register_user(delete_flow_request: DeleteFlowRequest):
    flowchart_operation = FlowChartOperation(model_adapter=model_adapter, postgresql_service=postgresql_service)
    result = await flowchart_operation.delete_flowchart(delete_flow_request)
    return result


@app.post("/query_flowlist")
async def register_user(query_flowlist: QueryFlowRequest):
    """
    User registration endpoint.
    """
    flowchart_operation = FlowChartOperation(model_adapter=model_adapter, postgresql_service=postgresql_service)
    result = await flowchart_operation.query_flowlist(query_flowlist)
    return result


@app.post("/get_bill")
async def register_user(register_request: RegisterRequest):
    pass
    return {"status": "success", "message": "User registered successfully"}


@app.get("/logo.png")
async def plugin_logo():
    """
    Return the plugin logo (48x48 PNG).
    """
    logo_path = Path("logo.png")
    if logo_path.exists():
        return FileResponse(logo_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Logo not found")

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest(request: Request):
    """
    Return the plugin manifest describing the plugin.
    """
    host = str(request.base_url)
    manifest_path = Path(".well-known/ai-plugin.json")
    if manifest_path.exists():
        with manifest_path.open(encoding="utf-8") as f:
            text = f.read().replace("PLUGIN_HOST", host)
            return JSONResponse(content=json.loads(text))
    raise HTTPException(status_code=404, detail="Manifest not found")

@app.get("/.well-known/openapi.yaml")
async def openapi_spec():
    """
    Return the OpenAPI spec for the plugin.
    """
    spec_path = Path(".well-known/openapi.yaml")
    if spec_path.exists():
        return FileResponse(spec_path, media_type="text/yaml")
    raise HTTPException(status_code=404, detail="OpenAPI spec not found")

@app.get("/static/{filename:path}")
async def serve_static(filename: str):
    """
    Serve static files from the 'static' directory.
    """
    static_dir = Path("static")
    file_path = static_dir / filename
    if file_path.exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# @app.get("/")
# async def serve_index():
#     """
#     Serve the index.html file.
#     """
#     index_path = Path("frontend/templates/index.html")
#     if index_path.exists():
#         return FileResponse(index_path)
#     raise HTTPException(status_code=404, detail="Index file not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")