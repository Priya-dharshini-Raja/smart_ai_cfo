import os

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql+psycopg2://priya19@#@localhost:5432/smart_ai_cfo")
SQLITE_URL = "sqlite:///../db/smart_ai_cfo.db"

DATABASE_URL = POSTGRES_URL if os.getenv("USE_POSTGRES", "0") == "1" else SQLITE_URL
