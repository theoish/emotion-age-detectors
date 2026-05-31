import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Mock user database (in production, use real database)
    USERS_DB = {
        "demo@example.com": {
            "email": "demo@example.com",
            "password": "demo123",  # In production, this should be hashed
            "name": "Demo User"
        }
    }

config = Config()