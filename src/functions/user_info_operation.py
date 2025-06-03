from src.utils.model_adapter import ModelAdapter
from src.utils.postgres_service import PostgresqlService
from src.models.request_model import LoginRequest, RegisterRequest
from src.utils.token_verification import create_access_token
from fastapi import HTTPException
from src.utils.config_loader import SERVICE_CONFIG,oauth
from src.utils.log_config import log_config
import requests,uuid
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
logger = log_config()

class UserInfoOperation:
    def __init__(self, model_adapter: ModelAdapter, postgresql_service: PostgresqlService) -> None:
        self.model_adapter = model_adapter
        self.postgresql_service = postgresql_service
        self.oauth = oauth
        self.service_config = SERVICE_CONFIG

    async def login_service(self, login_request: LoginRequest):
        username = login_request.username
        password = login_request.password
        # Verify username and password
        result = await self.postgresql_service.login_verification(username, password)
        if result['status'] == 'success':
            # Create JWT token
            access_token = create_access_token(data={"sub": username})
            avatar = result["result"]["avatar_url"]
            return {"status":"success","message":"no_user", "access_token": access_token, "token_type": "bearer", "avatar": avatar}
        elif result['status'] == 'no_user':
            return {"status":"success", "message":"no_user"}
        else:
            return {"status":"failure","message":"Invalid password"}

    async def google_redirect_callback(self, request):
        redirect_uri = self.service_config.google.google_redirect_uri
        logger.info(f"google login request is:{request.cookies}, redirect url is:{redirect_uri}")
        return await self.oauth.google.authorize_redirect(request, redirect_uri)

    async def google_oauth_callback(self,request):
        logger.info(f"request is:{request.session}")
        token = await self.oauth.google.authorize_access_token(request)
        logger.info(f"google login token is:{token}")
        nonce = request.session.get('nonce')
        user_info = await self.oauth.google.parse_id_token(token=token, nonce=nonce,
                                                           claims_options={
                                                               "iss": {"essential": True, "values": ["https://accounts.google.com"]},
                                                               "aud": {"essential": True, "value": self.service_config.google.client_id},
                                                               "exp": {"essential": True},
                                                               "nonce": {"essential": True},
                                                           })
        logger.info(f"user info is:{user_info}")
        email = user_info['email']
        user_name = user_info['name']
        user_pic = user_info['picture']
        result = await self.postgresql_service.check_user_exists(username=user_name)
        # Create JWT token
        access_token = create_access_token(data={"sub": user_name})
        if not result:
            await self.postgresql_service.insert_userInfo(username=user_name, email=email, avatar_url=user_pic)
        # return {"access_token": access_token, "token_type": "bearer", "avatar": user_pic}
        params = urlencode({
            "token": access_token,
            "avatar": user_pic,
            "username": user_name
        })
        frontend_redirect_url = f"{self.service_config.frontend_redirect_url}/introduction?{params}"
        return RedirectResponse(frontend_redirect_url)

    async def wechat_login(self):
        state = uuid.uuid4().hex
        wechat_qr_url = (
            f"https://open.weixin.qq.com/connect/qrconnect"
            f"?appid={self.service_config.wechat.wechat_app_id}&redirect_uri={self.service_config.wechat.wechat_redirect_uri}"
            f"&response_type=code&scope=snsapi_login&state={state}"
        )
        return {"qr_url": wechat_qr_url, "state": state}

    async def wechat_oauth_callback(self,code):
        token_url = (
            f"https://api.weixin.qq.com/sns/oauth2/access_token"
            f"?appid={self.service_config.wechat.wechat_app_id}&secret={self.service_config.wechat.wechat_app_secret}&code={code}&grant_type=authorization_code"
        )
        token_response = requests.get(token_url).json()

        if "errcode" in token_response:
            raise HTTPException(status_code=400, detail="Failed to authenticate with WeChat")

        access_token = token_response["access_token"]
        openid = token_response["openid"]

        user_info_url = (
            f"https://api.weixin.qq.com/sns/userinfo"
            f"?access_token={access_token}&openid={openid}"
        )
        user_info = requests.get(user_info_url).json()

        if "errcode" in user_info:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")

        # 检查 openid 是否已注册
        #todo check db whether user has been registered
        # for username, user in USER_DB.items():
        #     if user.get("openid") == openid:
        #         jwt_token = create_access_token(data={"sub": username})
        #         return {
        #             "access_token": jwt_token,
        #             "token_type": "bearer",
        #             "avatar": user["avatar"],
        #         }
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {
                    "message": "WeChat login successful, please bind or register an account.",
                    "wechat_user_info": user_info,
                }
            ),
        )


    async def register(self, register_request: RegisterRequest):
        username = register_request.username
        password = register_request.password
        result = await self.postgresql_service.check_user_exists(username)
        if result:
            return {"status": "fail", "message": "User already exist"}
            # raise HTTPException(status_code=400, detail="Username already exists")
        # Hash the password before storing it
        await self.postgresql_service.insert_userInfo(username=username, password=password)
        return {"status": "success", "message": "User registered successfully"}



