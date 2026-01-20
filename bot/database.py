from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, ConfigurationError
from datetime import datetime, timezone
from bot.config import MONGODB_URI, logger
import certifi

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.users = None
        self.connect()

    def connect(self):
        try:
            # Increased timeout to 30s to handle slow initial SSL handshakes
            self.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=30000, tlsCAFile=certifi.where())
            # Trigger a connection to verify
            self.client.admin.command('ping')
            
            # Explicitly set database to 'myewallet' as requested
            self.db = self.client['myewallet']
                
            self.users = self.db.users
            logger.info("Connected to MongoDB successfully. Database: myewallet")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            # We might want to retry or handle this gracefully
            self.client = None
            self.db = None
            self.users = None

    def add_user(self, user_id, username, first_name, last_name):
        if self.users is None:
            return
            
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            # We don't set last_activity here anymore to avoid updates on every /start
        }
        
        try:
            # Use update_one with $setOnInsert.
            # This ensures we ONLY write if the user does NOT exist.
            # If the user exists, NOTHING happens (no update).
            self.users.update_one(
                {"user_id": user_id},
                {
                    "$setOnInsert": {
                        **user_data,
                        "join_date": datetime.now(timezone.utc),
                        "last_activity": datetime.now(timezone.utc)
                    }
                },
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")

    def get_user(self, user_id):
        if self.users is None:
            return None
        return self.users.find_one({"user_id": user_id})

    def get_all_users(self):
        if self.users is None:
            return []
        return list(self.users.find({}))

    def count_users(self):
        if self.users is None:
            return 0
        return self.users.count_documents({})

# Global database instance
db = Database()
