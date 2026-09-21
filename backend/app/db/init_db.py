import logging

from app.db.database import Base, engine

logger = logging.getLogger(__name__)


def init_db():
    """
    Initialize database tables safely.
    Uses create_all which only creates tables that don't exist.
    Existing data is preserved.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialization completed successfully")
    except Exception:
        logger.exception("Database initialization failed")
        raise
