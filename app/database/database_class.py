from __future__ import annotations
from typing import Any, Sequence
from psycopg import AsyncConnection
from psycopg.abc import Query

from app.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self) -> None:
        self.user = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD
        self.host = settings.POSTGRES_HOST
        self.port = settings.POSTGRES_PORT
        self.db = settings.POSTGRES_DB

    async def get_connection(self) -> AsyncConnection:
        """Creates and returns a new async database connection."""
        try:
            conn = await AsyncConnection.connect(
                host=self.host,
                dbname=self.db,
                user=self.user,
                password=self.password,
                port=self.port,
                sslmode="require",
            )
            return conn
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise RuntimeError(f"Database connection error: {e}")

    async def fetch_one(self, query: Query, args: Sequence[Any] | None = None) -> Any | None:
        """Read 1 row."""
        try:
            async with await self.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args or ())
                    return await cur.fetchone()
        except Exception as e:
            logger.error(f"❌ fetch_one failed: {e}")
            raise

    async def fetch_all(self, query: Query, args: Sequence[Any] | None = None) -> list[Any]:
        """Read all rows."""
        try:
            async with await self.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args or ())
                    return await cur.fetchall()
        except Exception as e:
            logger.error(f"❌ fetch_all failed: {e}")
            raise

    async def execute_write(self, query: Query, args: Sequence[Any] | None = None) -> int:
        """
        Generic method for INSERT/UPDATE/DELETE.
        Returns the number of rows affected.
        """
        try:
            async with await self.get_connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args or ())
                    await conn.commit()
                    logger.info(f"✅ Query executed. Rows affected: {cur.rowcount}")
                    return cur.rowcount
        except Exception as e:
            logger.error(f"❌ Write operation failed: {e}")
            raise

    # Optional wrappers
    async def insert_row(self, query: Query, args: Sequence[Any] | None = None) -> int:
        return await self.execute_write(query, args)

    async def update_row(self, query: Query, args: Sequence[Any] | None = None) -> int:
        return await self.execute_write(query, args)

    async def delete_row(self, query: Query, args: Sequence[Any] | None = None) -> int:
        return await self.execute_write(query, args)
