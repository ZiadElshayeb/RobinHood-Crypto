import psycopg2
from app.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

class Database:

    def __init__(self):
        self.user = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD
        self.host = settings.POSTGRES_HOST
        self.port = settings.POSTGRES_PORT
        self.db = settings.POSTGRES_DB

    def get_connection(self):
        """Creates and returns a new database connection."""
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.db,
                user=self.user,
                password=self.password,
                port=self.port,
                sslmode='require'
            )
            return conn
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise RuntimeError(f"Database connection error: {e}")

    def fetch_one(self, query: str, args=None):
        """Read 1 row"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, vars=args)
                    result = cur.fetchone()
                    return result
        except Exception as e:
            logger.error(f"❌ fetch_one failed: {e}")
            raise

    def fetch_all(self, query: str, args=None):
        """Read all rows"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, vars=args)
                    results = cur.fetchall()
                    return results
        except Exception as e:
            logger.error(f"❌ fetch_all failed: {e}")
            raise

    def execute_write(self, query: str, *args) -> int:
        """
        Generic method for Insert, Update, DELETE.
        Returns the number of rows affected.
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, vars=args)
                    conn.commit() # Save changes
                    logger.info(f"✅ Query executed. Rows affected: {cur.rowcount}")
                    return cur.rowcount
        except Exception as e:
            logger.error(f"❌ Write operation failed: {e}")
            raise

    # Wrappers for specific actions (optional, but good for readability)
    def insert_row(self, query: str, *args):
        return self.execute_write(query, args)

    def update_row(self, query: str, *args):
        return self.execute_write(query, args)

    def delete_row(self, query: str, *args):
        return self.execute_write(query, args)
