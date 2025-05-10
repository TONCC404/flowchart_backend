from src.utils.model_adapter import ModelAdapter
from src.utils.postgres_service import PostgresqlService
from src.models.request_model import LoginRequest, RegisterRequest
from src.utils.token_verification import create_access_token
from fastapi import HTTPException
from authlib.integrations.starlette_client import OAuth
from src.utils.config_loader import SERVICE_CONFIG
import os



class UserInfoOperation:
    def __init__(self, model_adapter: ModelAdapter, postgresql_service: PostgresqlService) -> None:
        self.model_adapter = model_adapter
        self.postgresql_service = postgresql_service
        self.oauth = OAuth()
        self.service_config = SERVICE_CONFIG
        self.oauth.register(
            name='google',
            client_id=self.service_config.google.client_id,
            client_secret=self.service_config.google.client_secret,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            authorize_params=None,
            access_token_url='https://accounts.google.com/o/oauth2/token',
            access_token_params=None,
            refresh_token_url=None,
            client_kwargs={'scope': 'openid profile email'}
        )


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
        return await self.oauth.google.authorize_redirect(request, redirect_uri)

    async def google_oauth_callback(self,request):
        token = await self.oauth.google.authorize_access_token(request)
        user_info = await self.oauth.google.parse_id_token(request, token)
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



