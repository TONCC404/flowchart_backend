from src.utils.model_adapter import ModelAdapter
from src.utils.postgres_service import PostgresqlService
from src.models.request_model import LoginRequest, RegisterRequest
from src.utils.token_verification import create_access_token
from fastapi import HTTPException
from src.utils.config_loader import SERVICE_CONFIG,oauth
from src.utils.log_config import log_config
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
            return {"access_token": access_token, "token_type": "bearer", "avatar": avatar}
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")

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
        user_pic = user_name['picture']
        #todo judge whether user in pgdb

        return {"message": "Login successful", "user_info": user_info}

    async def register(self, register_request: RegisterRequest):
        username = register_request.username
        password = register_request.password
        result = await self.postgresql_service.check_user_exists(username)
        if result:
            return {"status": "fail", "message": "User already exist"}
            # raise HTTPException(status_code=400, detail="Username already exists")
        # Hash the password before storing it
        await self.postgresql_service.insert_userInfo(username, password)
        return {"status": "success", "message": "User registered successfully"}



