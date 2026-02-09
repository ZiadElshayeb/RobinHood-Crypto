from app.database.database_class import Database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_tables():
    """
    Creates the necessary tables in the database if they don't exist.
    """
    db = Database()
    
    # 1. SQL for Trade History
    create_trades_table = """
    CREATE TABLE IF NOT EXISTS crypto_trade_history (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(50) NOT NULL,
        side VARCHAR(10) NOT NULL,
        quantity FLOAT NOT NULL,
        price FLOAT NOT NULL,
        amount_usd FLOAT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reason TEXT,
        is_open BOOLEAN DEFAULT TRUE,
        profit_loss FLOAT
    );
    """
    
    # 2. SQL for System Logs
    create_logs_table = """
    CREATE TABLE IF NOT EXISTS crypto_system_logs (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        level VARCHAR(20),
        message TEXT
    );
    """

    try:
        logger.info("🔨 Creating 'trade_history' table...")
        db.execute_write(create_trades_table)
        
        logger.info("🔨 Creating 'system_logs' table...")
        db.execute_write(create_logs_table)
        
        logger.info("✅ Database initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")

if __name__ == "__main__":
    init_tables()