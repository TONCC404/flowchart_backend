import os
import logging

logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_prompt(prompt_name: str) -> str:
    prompt_path = os.path.join(ROOT_DIR, "prompt", prompt_name)
    with open(prompt_path, 'r',encoding='utf-8') as file:
        prompt = file.read()
        return prompt
