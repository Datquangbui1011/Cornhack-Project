import logging
from supabase import create_client
from core.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 


def get_supabase_client():
    """
    Initialize the Supabase client using the appropriate credentials based on the environment.
    """
    db_url = settings.DB_URL
    db_key = settings.DB_KEY
    logger.info("Initializing Supabase client in development mode.")

    client = create_client(db_url, db_key)
    logger.info("Supabase client initialized successfully.")
    return client

supabase = get_supabase_client()
