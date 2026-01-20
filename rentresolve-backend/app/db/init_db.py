from .session import engine, Base
from .models import User, Issue, Message, EmailLog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        logger.info("Please ensure PostgreSQL is running and the database 'rentresolve' exists.")

if __name__ == "__main__":
    init_db()
