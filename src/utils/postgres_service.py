import logging

from src.models.config_model import ServiceConfig
from src.utils.model_adapter import ModelAdapter
import asyncpg
import psycopg2
import uuid
from datetime import datetime
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

class PostgresqlService:
    def __init__(self, service_config: ServiceConfig) -> None:
        self.pool = None
        self.conn = None
        self.service_config = service_config
        self.model_adapter = ModelAdapter(service_config)
        # self.embedding_config = service_config.postgresql.embedding_model
        self.connection = None

    async def __aenter__(self):
        if not self.pool:
            logger.info("Connection pool has been created.")
            await self.create_pool()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        logger.info("Connection pool has been closed.")
        await self.close_pool()

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            host=self.service_config.postgresql.host,
            port=self.service_config.postgresql.port,
            user=self.service_config.postgresql.user,
            password=self.service_config.postgresql.password,
            database=self.service_config.postgresql.database,
            max_size=2,
            min_size=0
        )

    async def create_connection(self):
        self.connection = await asyncpg.connect(
            host=self.service_config.postgresql.host,
            port=self.service_config.postgresql.port,
            user=self.service_config.postgresql.user,
            password=str(self.service_config.postgresql.password),
            database=self.service_config.postgresql.database
        )

    async def close_pool(self):
        if self.pool:
            await self.pool.close()
            print("Connection pool closed.")

    async def check_user_exists(self, username):
        if not self.connection:
            await self.create_connection()
        try:
            query = "SELECT EXISTS (SELECT 1 FROM users WHERE username = $1);"
            exists = await self.connection.fetchval(query, username)
            return exists
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if self.connection:
                await self.connection.close()

    async def insert_userInfo(self, username, password=None, org=None,team = None, industry = None, collaborators = None, email=None, phone=None, avatar_url=None, balance=0, currency="USD"):

        try:
            insert_query = """
            INSERT INTO users (
                id, username, org, team, industry, collaborators, password_hash, email, phone, avatar_url, balance, currency, is_active, created_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14
            )
        """
            user_id = str(uuid.uuid4())
            created_at = datetime.now()
            is_active = True
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password=None
            if password:
                hashed_password = pwd_context.hash(password)
            if not self.connection or self.connection.is_closed():
                await self.create_connection()
            await self.connection.execute(
                insert_query,
                user_id, username, org, team, industry, collaborators, hashed_password, email, phone, avatar_url, balance, currency, is_active, created_at
            )

            print(f"User {username} inserted successfully.")

        except Exception as e:
            print(f"Error inserting user: {e}")
        finally:
            if self.connection:
                await self.connection.close()


    async def login_verification(self, username, password=None):
        try:
            if not self.connection or self.connection.is_closed():
                await self.create_connection()
            query = "SELECT id, password_hash, avatar_url, org, role, username FROM users WHERE username = $1"
            user_record = await self.connection.fetchrow(query, username)
            if not user_record:
                return {"status": "no_user", "message": "Invalid username or password"}
            stored_password_hash = user_record["password_hash"]
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            if pwd_context.verify(password, stored_password_hash):
                return {"status": "success", "message": "Login successful", "result": user_record}
            else:
                return {"status": "error", "message": "Invalid username or password"}

        except Exception as e:
            print(f"Error during login: {e}")
            return {"status": "error", "message": "Internal server error"}
        finally:
            if self.connection:
                await self.connection.close()

    async def save_flow(self, flow_id, name, data, user_id):
        try:
            if not self.pool:
                logger.info("Connection pool has been created.")
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    insert_query = """
                        INSERT INTO flowcharts (flow_id, name, data, user_id, updated_at)
                        VALUES ($1, $2, $3, NOW())
                        ON CONFLICT (flow_id)
                        DO UPDATE SET name = EXCLUDED.name, data = EXCLUDED.data, updated_at = NOW()
                        """
                    await conn.execute(
                        insert_query,
                        flow_id, name, data, user_id
                    )

                    print(f"flow saved successfully.")
            return {"status": "success"}

        except Exception as e:
            print(f"error flow saving: {e}")
            return {"status": "fail"}


    async def delete_flow(self, flow_id):
        try:
            if not self.connection or self.connection.is_closed():
                await self.create_connection()
            query = "UPDATE flowcharts SET is_deleted = TRUE, updated_at = NOW() WHERE flow_id = $1"
            delete_flow = await self.connection.fetchrow(query, flow_id)
            return {"status": "success", "message": "Login successful", "result": delete_flow}
        except Exception as e:
            print(f"Error during login: {e}")
            return {"status": "error", "message": "Internal server error"}
        finally:
            if self.connection:
                await self.connection.close()


    async def query_flowlist(self, user_id):
        try:
            if not self.connection or self.connection.is_closed():
                await self.create_connection()
            query = "SELECT * FROM flowcharts WHERE user_id = $1 AND is_deleted = FALSE"
            query_result = await self.connection.fetchrow(query, user_id)
            return {"status": "success", "message": "Login successful", "result": query_result}
        except Exception as e:
            print(f"Error during login: {e}")
            return {"status": "error", "message": "Internal server error"}
        finally:
            if self.connection:
                await self.connection.close()