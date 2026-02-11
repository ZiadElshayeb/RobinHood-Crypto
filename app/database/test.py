import asyncio
import sys
from app.database.database_class import Database

# Fix for Windows async psycopg compatibility
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    db = Database()
    
    # Insert
    await db.insert_row(
        "INSERT INTO crypto_system_logs (level, message) VALUES (%s, %s)",
        ("INFO", "Test log message")
    )
    
    # Fetch
    rows = await db.fetch_all("SELECT * FROM crypto_system_logs WHERE level = %s", ("INFO",))
    print(rows)

if __name__ == "__main__":
    asyncio.run(main())