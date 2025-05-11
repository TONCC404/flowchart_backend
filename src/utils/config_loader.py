import os
from src.models.config_model import ServiceConfig
import yaml
import sys
import logging

logger = logging.getLogger(__name__)
args = sys.argv

def config_loader(path: str) -> ServiceConfig:
    with open(path, 'r') as file:
        prime_service = yaml.safe_load(file)
        return ServiceConfig.model_validate(prime_service)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR,"config.yaml")
LOG_PATH = os.path.join(ROOT_DIR, "log.ini")
SERVICE_CONFIG = config_loader(CONFIG_PATH)

from authlib.integrations.starlette_client import OAuth
oauth = OAuth()

service_config = SERVICE_CONFIG
oauth.register(
    name='google',
    client_id=SERVICE_CONFIG.google.client_id,
    client_secret=SERVICE_CONFIG.google.client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    # authorize_url='https://accounts.google.com/o/oauth2/auth',
    # access_token_url='https://accounts.google.com/o/oauth2/token',
    client_kwargs={'scope': 'openid profile email'},
)
