import logging
import os

database_url = os.getenv("DATABASE_URL", "sqlite://")
address = ('0.0.0.0', 8000)
prime = int(os.getenv("PRIME", 23))
generator = int(os.getenv("GENERATOR", 2))
LOG_LEVEL = logging.INFO


