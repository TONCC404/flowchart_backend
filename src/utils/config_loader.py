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
