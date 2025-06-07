import logging

from src.models.config_model import ServiceConfig
from src.utils.model_adapter import ModelAdapter
import random
import string
from email.mime.text import MIMEText
from email.header import Header
import smtplib


logger = logging.getLogger(__name__)

class MailService:
    def __init__(self, service_config: ServiceConfig) -> None:
        self.service_config = service_config
        self.model_adapter = ModelAdapter(service_config)

    async def send_verification_code(self, to_email, length = 6):
        code = ''.join(random.choices(string.digits, k=length))
        subject = "您的验证码"
        body = f"您的验证码是：{code}，请在5分钟内使用。"

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = Header(self.service_config.mail.username)
        msg['To'] = Header(to_email)
        msg['Subject'] = Header(subject, 'utf-8')

        try:
            if self.service_config.mail.port == 465:
                server = smtplib.SMTP_SSL(self.service_config.mail.host, self.service_config.mail.port)
            else:
                server = smtplib.SMTP(self.service_config.mail.host, self.service_config.mail.port)
                server.starttls()
            server.login(self.service_config.mail.username, self.service_config.mail.password)
            server.sendmail(self.service_config.mail.username, [to_email], msg.as_string())
            server.quit()
            print(f"验证码已发送到 {to_email}，验证码为 {code}")
            return code
        except Exception as e:
            print("发送失败：", e)
            return None